from lxml.html import fromstring

def parse_input(input):
    tree = fromstring(input)
    return tree.text_content()

if __name__ == '__main__':
    pass