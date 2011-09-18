from prettytable import PrettyTable

#import prettytable

BOX_WIDTH = 150

def fill(title):
    return "%s%s" % (title, " "*(BOX_WIDTH-len(title)))

def print_header():
    print "\n",
    title = fill("This puppet kick tool(Pkick) has super power!")
    table = PrettyTable([title])
    table.add_row(["Please wait ..."])
    print(table)
    print "\n",

def print_box(title, rows):
    """
    Args:
        title: the title column
        rows: list, each element is a row
    """
    title = fill(title)
    table = PrettyTable([title])
    for row in rows:
        table.add_row([row,])
    print(table)
    
def print_node_box(node_list):
    print_box("The node to be kicked:", node_list)
    
def print_seprate_line():
    content = "v" + "="*160 + "v"
    print content

def print_pre_node_box(succ, node_list):
    if succ:
        print_box("Previous successful nodes:", node_list)
    else:
        print_box("Previous failed nodes:", node_list)

def print_errmsg(errmsg):
    print_box("error parameter:", [errmsg])

if __name__ == '__main__':
#    print_box("These node will be kicked:")
#    print_header()
    print_box("abc", ['d','e'])
