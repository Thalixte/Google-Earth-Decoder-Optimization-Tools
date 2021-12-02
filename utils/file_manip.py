######################################################
# File manipulation methods
###################################################### 
def line_prepender(filename, line):
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip("\r\n") + "\n" + content)


######################################################
# File replacement methods
###################################################### 
def replace_in_file(file, text, replacement):
    updated_file = open(file, "rt")
    data = updated_file.read()
    data = data.replace(text, replacement)
    updated_file.close()
    updated_file = open(file, "wt")
    updated_file.write(data)
    updated_file.close()


##########################################################################
# function to pretty print the XML code
##########################################################################
def pretty_print(element, level=0):
    '''
    Function taken from elementTree site:
    http://effbot.org/zone/element-lib.htm#prettyprint

    '''
    indent = '\n' + level * '  '
    if len(element):
        if not element.text or not element.text.strip():
            element.text = indent + '  '

        if not element.tail or not element.tail.strip():
            element.tail = indent

        for element in element:
            pretty_print(element, level + 1)

        if not element.tail or not element.tail.strip():
            element.tail = indent

    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = indent

    return element
