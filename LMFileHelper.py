import re
import json
class LMFileHelper:

    text = []   #text in the original source code
    style = {}  #style in the style text

    def __init__(self, source_filename = None, style_filename = None):
        self.source_filename = source_filename
        self.file_obj = None
        self.style_filename = style_filename
        self.style_file = None

    # read the source code from the file
    # Using <empty> to replace \n so that it won't be strip when handling
    def read_source_code(self):
        if self.source_filename is None:
            return None
        self.file_obj = open(self.source_filename)
        reg = re.compile(r'\s*\n')
        for line in self.file_obj:
            if reg.match(line):
                self.text.append('<empty>')
            else:
                self.text.append(line.strip())

    def read_style(self):
        if style_filename is None:
            return None
        self.style_file = open(self.style_filename)
        self.style = json.loads(''.join([line for line in self.style_file]))


# code1 = LMFileHelper(r'C:\Users\Xuanyu\Desktop\hahaha.txt',r'C:\Users\Xuanyu\Desktop\lexical\1.style')
# code1.read_source_code()
# code1.read_style()
# print code1.text , '\n'
# print code1.style
