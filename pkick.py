#!/usr/bin/env python
# encoding: utf-8
#
# This script is a tool wrap for "puppet kick" for batch push puppet client update
#
from cachehandler import CacheHandler
from colorize import Colorize
from optparse import OptionParser
from parser import Parser
from utils import print_header, print_node_box, print_pre_node_box, print_errmsg
import copy
import json
import os
import re
import socket
import subprocess
import threadpool


__authors__  = ['jacky wu <jacky.wucheng@gmail.com>', ]
__version__  = 1.0
__date__     = "2011-9-13 上午11:29:47"



#===============================================================================
# some global macro
NODE_CACHE = "var/node_cache"
RESULT_CACHE = "var/result_cache"
#===============================================================================


class Pkick(object):

    def run_cmd(self, cmd):
        '''
        return: (stdout, stderr)
        '''
        pobj = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return pobj.communicate()
    
    def get_node_list_from_puppet(self):
        cmd = "puppet cert list --all"
        result = self.run_cmd(cmd)
        node_list = [node for node in result[0].split("\n")]
        tidy_node_list = []
        for node_str in node_list:
            if node_str:
                tidy_node_list.append( node_str.split()[1] )
        return tidy_node_list
        
        
    def get_all_node(self):
        if os.path.exists(NODE_CACHE):
            tidy_node_list = CacheHandler.unserialize(NODE_CACHE)
        else:
            tidy_node_list = self.update_node_cache()
            
        return tidy_node_list
                
    def get_previous_node(self, succ=True, append_err=True):
        """ get previous nodes who were kicked successfully or failed
        Args:
            succ: if True return nodes who is kicked successfully
                  if False return nodes who is kicked failed
        """
        result_cache = CacheHandler.unserialize(RESULT_CACHE)
        nodes = []
        for result in result_cache:
            # each element is [host, stdout, stderr, status]
            host = result[0]
            err = result[2]
            if succ:
                if result[3]: nodes.append(host)
            else:
                if not result[3]: 
                    if append_err:
                        nodes.append([host,err])
                    else:
                        nodes.append(host)
                
        return nodes
    
    
    def update_node_cache(self):
        tidy_node_list = self.get_node_list_from_puppet()
        CacheHandler.serialize(NODE_CACHE, tidy_node_list)
        return tidy_node_list
     
    def filter_self(self, nodes):
        self_node_name = socket.gethostname()
        cp_nodes = copy.deepcopy(nodes)
        if self_node_name in cp_nodes:
            cp_nodes.remove(self_node_name)
        return cp_nodes
            
    def filter_node(self, filter_str):
        all_node = self.get_all_node()
        if (not filter_str) or (not filter_str.strip()):
            filtered_node = all_node
        else:
            filtered_node = [node for node in all_node if re.search(filter_str, node)]

        filtered_node = self.filter_self(filtered_node)
        
        return filtered_node

    def kick(self, hosts):
        hosts_count = len(hosts.split(" "))
        if hosts_count > 1:
            parallel = hosts_count
        else:
            parallel = 1
        cmd = "puppet kick --ping --parallel {parallel} {hosts}".format(parallel=parallel, hosts=hosts)
        
        return list((hosts,) + self.run_cmd(cmd))


################### global threadpool result callback function ###################
RESULT_Q = []
def enqueue(request, result):
    parser = Parser()
    RESULT_Q.append(parser.append_status(result))

    
def puppet_kick(node_list):
    # thread pool
    pkick = Pkick()
    poolsize = 20
    pool = threadpool.ThreadPool(poolsize)
    requests = threadpool.makeRequests(pkick.kick, node_list, enqueue)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    CacheHandler.write(RESULT_CACHE, json.dumps(RESULT_Q))
    

def main():
    ''' main logical flow
    '''
    usage = "usage: %prog [options] arg"
    
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--update_cache", dest="update_cache", action="store_true", 
                      help="get all puppet client node from puppet master and "
                      "cache them locally")
    parser.add_option("-f", "--failed_node", dest="failed_node", action="store_true",
                      help="show nodes whose kick operation is failed. This param "
                      "is only effective before a new kick operation")
    parser.add_option("-s", "--succ_node", dest="succ_node", action="store_true",
                      help="show nodes whose kick operation is successful. This "
                      "param is only effective before a new kick operation")
    parser.add_option("-m", "--manual", dest="manual", action="store_true", 
                      help="show manual")
    parser.add_option("-p", "--pattern", dest="pattern", default=None,
                      help="The pattern is used to filter nodes from all_node_list")
    parser.add_option("-d", "--display", dest="display", action="store_true",
                      help="display the nodes who will be kicked, but not do it "
                      "in fact")
    
    (options, args) = parser.parse_args()
    print_header()
    
    pkick = Pkick()
    
    
    if options.update_cache:
        Pkick().update_node_cache()
        exit()
    
    if options.succ_node and options.failed_node:
        print_errmsg("-f/--failed_node and -s/--succ_node can not be used together")
        exit()

    if options.succ_node:
        succ_nodes = pkick.get_previous_node(True)
        print_pre_node_box(True, succ_nodes)
        exit()
    
    if options.failed_node:
        failed_nodes = pkick.get_previous_node(False, append_err=True)
        failed_node_err = ["%s -->error: %s" % (node[0].strip(), node[1].strip()) for node in failed_nodes]
        print_pre_node_box(False, failed_node_err)
        exit()

    node_list = pkick.filter_node(options.pattern)

    if options.display:
        print_node_box(node_list)
        exit()
    else:
        puppet_kick(node_list)
        color = Colorize()
        color.colorize_output(RESULT_Q, node_list)
        exit()


if __name__ == "__main__":
    main()
