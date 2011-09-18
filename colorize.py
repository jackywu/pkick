from termcolor import colored
from utils import print_header, print_box, print_seprate_line, print_node_box
import re

class Colorize(object):

    def colorize_failed_str(self, input):
        output = input.replace('Failed', colored('Failed', 'red', attrs=['blink',]))
        return output

    def colorize_exit_code(self, input):
        m = re.search(r'exit code ([1-9])', input)
        if m:
            retcode = m.groups()[0]
            match_str = m.group()

            if int(retcode) != 0:
                output = input.replace(match_str, colored(match_str, 'red', attrs=['blink',]))
                return output
        else:
            return input


    def colorize_fail(self, input):
        ''' Tt's a wrap for colorize_failed_str and colorize_exit_code
        This method will highlight all the error text
        '''
        output = self.colorize_failed_str(input)
        output = self.colorize_exit_code(output)

        return output


    def colorize_error(self, input):
        output = colored(input, 'cyan', attrs=['blink'])
        return output

    def colorize_attention_fail(self, input):
        output = colored("^ %s ^\n" % input, 'yellow', attrs=['blink',])
        return output

    def colorize_attention_succ(self, input):
        output = colored("^ %s ^\n" % input, 'cyan', attrs=['blink',])
        return output

    def colorize_succ(self, input):
        output = colored(input, 'magenta')
        return output
      
    def colorize_output(self, result_q, node_list):
        """colorize the puppet kick result text
        Args:
             result_q : list, every result of each node
            node_list : list, the node list who is to be kicked
        """
        # step: display the object which the tool will deal with
        print_node_box(node_list)
        print_seprate_line()

        # step: colorize the result

        for result in result_q:

            host, stdout, stderr, kick_status = result

            if not kick_status:
                # error handler step
                output = "\n".join([self.colorize_fail(stdout),
                                    self.colorize_fail(stderr),
                                    self.colorize_attention_fail("%s %s %s" %
                                                             ("="*20,
                                                              "Puppet kick %s failed" % host,
                                                              "="*20))])

            else:
                # succ handler step
                output = "\n".join([self.colorize_succ(stdout),
                                   self.colorize_attention_succ("%s %s %s" % 
                                                           ("-"*20,
                                                            "Puppet kick %s succ" % host,
                                                            "-"*20))])

            print(output)
