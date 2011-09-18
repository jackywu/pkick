from texttable import Texttable

BOX_WIDTH = 150

def fill(title):
    return "%s%s" % (title, " "*(BOX_WIDTH-len(title)))

def print_box(title, rows):
    """
    Args:
        title: the title column
        rows: list, each element is a string
    """
    title = fill(title)
    
    table = Texttable()
    table.set_cols_align(["l"])
    table.set_cols_valign(["m"])
    
    table.add_row([title])
#    table.add_row(["\n".join(rows)])
    for row in rows:
        table.add_row([row])
    print(table.draw())
    

def print_header():
    title = "This puppet kick tool(Pkick) has super power!"
    row = "Please wait ..."
    print_box(title, [row])
    print_seprate_line()
    
    
def print_node_box(node_list):
    print_box("The nodes to be kicked:", node_list)
    
def print_seprate_line():
    content = "\nv" + "="*160 + "v\n"
    print(content)

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
