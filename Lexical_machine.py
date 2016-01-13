# -*- coding: utf-8 -*-

import json
import re
import sys

# replace an element in a list with a list
def list_replace(list, index, content_for_replace):
    list[index:index+1] = content_for_replace
    return index + len(content_for_replace)

def word_clean(li):
    return [x.strip() for x in list(filter(lambda x : x != '', li))]

class SystaxError(Exception):
    pass

class LexicalMachine:

    text = [] # A list to store every line of source code
    lines = 0
    style = {}
    global_machine = None
    info = ''

    def __init__(self, source_filename, style_filename):

        self.source_filename = source_filename
        self.style_filename = style_filename

        self.source_file = None
        self.style_file = None

        self.output_filename = self.source_filename[:-2] + '_output.c'
        self.output_info = self.source_filename[:-2] + '_info.txt'

    # Read the source code from the file
    # Using <empty> to replace \n so that it won't be strip when handling
    def read_source_code(self, file):
        reg = re.compile(r'\s*\n')
        for line in file:
            if reg.match(line):
                self.text.append('<empty>') 
            else:
                self.text.append(line.strip()) # delete whitespace
        # print self.text

    # Read the style file
    def read_style(self, file):
        self.style = json.loads(''.join([line for line in file]))
        # for key, value in self.style.items():
        #     print key, ':',  value

    # Check style file input, if there is not any coresponding parameter,
    # the program will use a default value
    # instead of using `get` as there is several levels for a dictionary
    def style_check(self):

        # 4.1.1.1 Check the function and left parenthesis
        if self.style.has_key('function'):
            if not self.style['function'].has_key('left_parenthesis_blank'):
                self.style['function']['left_parenthesis_blank'] = False
            if not self.style['function'].has_key('left_parenthesis_newline'):
                self.style['function']['left_parenthesis_newline'] = False
        else:
            self.style['function'] = {
                'left_parenthesis_blank': False,
                'left_parenthesis_newline': False,
            }

        # 4.1.1.2 Check blank existence in the right of the left parenthesis
        # and the left of the right parenthesis
        if 'parenthesis' in self.style:
            if not self.style['parenthesis'].has_key('left_parenthesis_right_blank'):
                self.style['parenthesis']['left_parenthesis_right_blank'] = False
            if not self.style['parenthesis'].has_key('right_parenthesis_left_blank'):
                self.style['parenthesis']['right_parenthesis_left_blank'] = False
        else:
            self.style['parenthesis'] = {
                'left_parenthesis_right_blank': False,
                'right_parenthesis_left_blank': False,
            }

        # 4.1.1.3 tabstop, default is 4
        if not self.style.has_key('tabstop'):
            self.style['tabstop'] = 4

        # 4.1.1.4 blank character after special character
        if not self.style.has_key('special_character_blank'):
            self.style['special_character_blank'] = [',', ';']

        # 4.1.1.5 and 4.1.1.8
        # 4.1.1.5, 'brace_for_block' determine that no matter how many sentences
        #         in the block, there should always be braces
        # 4.1.1.8, 'left_brace_new_line', if it is true, then, the left brace should
        #         be in the new line
        if self.style.has_key('brace'):
            if not self.style['brace'].has_key('brace_for_block'):
                self.style['brace']['brace_for_block'] = True
            if not self.style['brace'].has_key('left_brace_new_line'):
                self.style['brace']['left_brace_new_line'] = True
        else:
            self.style['brace'] = {
                'brace_for_block': True,
                'left_brace_new_line': True,
            }

        # 4.1.1.6 'delete_empty_statement', it is true when empty statement should
        #         always be deleted
        if not self.style.has_key('delete_empty_statement'):
            self.style['delete_empty_statement'] = True

        # 4.1.1.7 'one_statement_per_line', every statement occupies one line
        if not self.style.has_key('one_statement_per_line'):
            self.style['one_statement_per_line'] = True

    # ignore the comment; Block comments in /* */ or line comments after //
    # set all the comment line with ""
    def comment_delete(self):

        # Three regrex expressions, corresponding to three comment status
        block_comment_start = re.compile(r'([\s\S]*)/\*[\s\S]*') # "/*"
        block_comment_end = re.compile(r'[\s\S]*\*/([\s\S]*)') # "*/"
        line_comment_start = re.compile(r'([\s\S]*)//[\s\S]*') # "//"
        class UnexpectedEndofComment(Exception):
            pass

        class NestingofBlockComment(Exception):
            pass

        # status, "No": no comment;
        #         "BLock": block comment;
        status = "No"

        num = 0

        for line in self.text:
            block_match = block_comment_start.match(line)
            line_match = line_comment_start.match(line)
            end_match = block_comment_end.match(line)

            # /* // */ or /* */ // or // /* */ etc. 6 kinds of combinations
            if status == "No" and block_match and line_match and end_match:
                line_start_pos = line.index('//')
                block_start_pos = line.index('/*')
                block_end_pos = line.index('*/')

                # `//` is in the front, ignoring all behind `//`
                if min(line_start_pos, block_start_pos, block_end_pos) == line_start_pos:
                    self.text[num] = line_match.groups()[0]

                # `/*` is in the front, two conditions:
                # .../* // */...
                # .../* */...//
                # should both be extracted properly
                elif min(line_start_pos, block_start_pos, block_end_pos) == block_start_pos:
                    if block_end_pos > line_start_pos:
                        self.text[num] = block_match.groups()[0] + end_match.groups()[0]
                    else:
                        self.text[num] = block_match.groups()[0] + line[block_end_pos+2:line_start_pos]

                # `*/` is in the front and the status is `No`, throw an exception
                else:
                    raise UnexpectedEndofComment("Unexpected End of Comment in line({})".format(num+1))

            # only /* and //, when status is `No`
            elif status == "No" and block_match and line_match:
                line_start_pos = line.index('//')
                block_start_pos = line.index('/*')

                # `//` is in the front
                if line_start_pos < block_start_pos:
                    self.text[num] = line_match.groups()[0]
                else:
                    self.text[num] = block_match.groups()[0]
                    status = "Block"

            # `//` and `*/`, when status is `No`
            elif status == "No" and line_match and end_match:
                line_start_pos = line.index('//')
                block_end_pos = line.index('*/')

                if block_end_pos < line_start_pos:
                    raise UnexpectedEndofComment("Unexpected End of Comment in line({})".format(num+1))
                else:
                    self.text[num] = line_match.groups()[0]

            # `/*` and `*/`, when status is `No`
            elif status == "No" and block_match and end_match:
                block_start_pos = line.index('/*')
                block_end_pos = line.index('*/')
                if block_end_pos > block_start_pos:
                    raise UnexpectedEndofComment("Unexpected End of Comment in line({})".format(num+1))
                else:
                    self.text[num] = block_match.groups()[0] + end_match.groups()[0]

            elif status == "No" and line_match:
                self.text[num] = line_match.groups()[0]

            elif status == "No" and block_match:
                self.text[num] = block_match.groups()[0]
                status = "Block"

            elif status == "No" and end_match:
                raise UnexpectedEndofComment("Unexpected End of Comment in line({})".format(num+1))

            elif status == "No":
                pass

            elif status == "Block" and block_match:
                raise NestingofBlockComment("Nesting of Block Comment found in line({})".format(num+1))

            elif status == "Block" and end_match:
                status = "No"
                self.text[num] = end_match.groups()[0]

            else:
                self.text[num] = ''

            num += 1
            # print self.text
        self.text = word_clean(self.text)

    # 4.1.1.1 the First Condition
    @staticmethod
    # This method deletes the blank before the left parenthesis
    # Trick: Four matches, ignore the blank
    def function_left_parenthesis_blank(line):
        # 单词字符 若干空白字符 一次
        reg = re.compile(r'(\w+)[\s\*]+(\w+|\w+::\w+)\s*(\([\w\s,\*]*?\))([\s\S]*)')
        reg_match = reg.match(line)
        if reg_match:
            groups = reg_match.groups()
            print groups
            print groups[0]+' '+''.join(groups[1:])
            return groups[0]+' '+''.join(groups[1:])
        else:
            return line

    # 4.1.1.1 the Second Condition
    @staticmethod
    def function_left_parenthesis_newline(line1, line2):
        reg1 = re.compile(r'(\w+)[\s\*]+(\w+|\w+::\w+)\s*')
        reg2 = re.compile(r'\s*(\([\w\s,\*]*?\))([\s\S]*)')
        reg1_match = reg1.match(line1)
        reg2_match = reg2.match(line2)
        if reg1_match and reg2_match:
            return reg1_match.groups()[0]+' '+reg1_match.groups()[1]+''.join(reg2_match.groups()), ''
        else:
            return line1, line2

    # 4.1.1.2
    # Clear the blank in the right of the left parenthesis and the left of the right parenthesis
    # the first kind, there is blank, but still in the same line
    @staticmethod
    def parenthesis_blank(line):
        line = re.sub(r'\(\s+', '(', line)
        line = re.sub(r'\s+\)', ')', line)
        return line

    @staticmethod
    def left_right_parenthesis_blank(line):
        line = re.sub(r'\(\s+', '(', line)
        return line

    @staticmethod
    def right_left_parenthesis_blank(line):
        line = re.sub(r'\s+\)', ')', line)
        return line

    # 4.1.1.2
    # Clear the blank in the right of the left parenthesisi and the left of the right parenthesis
    # the second kind, there is blank, but in a new line
    @staticmethod
    def parenthesis_new_line(line1, line2):
        reg1 = re.compile(r'[^\(]*\([^\(]*')
        reg2 = re.compile(r'[^\)]*\)[^\)]*')
        if reg1.match(line1) and reg2.match(line2) and \
           line1.count('(') > line1.count(')') and \
           line2.count(')') > line2.count('('):
            return LexicalMachine.parenthesis_blank(line1+line2), ''
        else:
            return line1, line2

    # 4.1.1.4
    # Add blank to some special characters
    # it will use the list of special characters stored in the class attribute `style`
    # so it is not static method
    def special_character_blank(self, line):
        for character in self.style['special_character_blank']:
            line = re.sub('\s*'+character+'\s*', character+' ', line)
        return line.strip()

    # 4.1.1.7
    # as C code ends every lineLie with a colon, so here colon split is effective
    # Exclude the `for` loop
    # Warning: this funciton did not change the original list, but split the input line
    @staticmethod
    def multiple_code_split(line):
        if line.find("for") == -1:
            split_line =  re.sub(r';', ";\n", line).split('\n')
        else:
            li = re.findall(r'for\s*\([\s\S]+?\)', line)
            end = 0
            split_line = []
            # find the for loop first, then using the for loop to devide the line into pieces
            # for every pieces, using colon-split to get multiple lines
            index = line.index(li[0])
            split_line = split_line + re.sub(r';', ';\n', line[0:index]).split('\n')
            for loop in li:
                index = line.index(loop)
                if loop == li[-1]:
                    end = len(line)
                else:
                    end = line.index(li[li.index(loop)+1])
                part_split = re.sub(r';', ';\n', line[index + len(loop):end]).split('\n')
                part_split[0] = loop + part_split[0]
                split_line = split_line + part_split
        return word_clean(split_line)

    # 4.1.1.7
    # This function uses the result from @function multiple_code_split to replace the original line
    def multiple_code_split_and_replace(self):
        index = 0
        while index < len(self.text):
            index = list_replace(self.text, index, LexicalMachine.multiple_code_split(self.text[index]))

    # According to the requirements, there are actually some global feature such as:
    # 4.1.1.5 All the if/else/for should be followed by a left brace in the new line,
    # 4.1.1.8 All the left brace should be in the new line
    # 4.1.1.3 Analyze and correct the indent for all the lines
    # 4.1.3 Analyze the function caller and calling relations
    # These functions can't be realized locally, thus, using a unique inner class to handle.
    class GlobalCharacterAnalysis:

        def __init__(self, text, tabstop):
            self.text = text
            self.tabstop = tabstop
            self.reg_if = re.compile(r'\s*if\s*\([\s\S]*')
            self.reg_elseif = re.compile(r'\s*else\s+if\s*\([\s\S]*')
            self.reg_else = re.compile(r'\s*else\s*')
            self.reg_while = re.compile(r'\s*while\s*\([\s\S]*')
            self.reg_for = re.compile(r'\s*for\s*\([\s\S]*')
            self.left_brace = {}
            self.right_brace = {}
            self.left_brace_accumulate = 0

            # Delete vacuum lines
            self.vacuum_lines = []

            # Identify functions and their calling relationships
            self.functions = ['main']
            self.calling_relationship = {}
            self.called_relationship = {}
            self.exclude_words = ['for','while','if','else','printf','scanf',]

        # Using recursive to detect special keywords eg. if/else/for/while
        # the recursive to do as below:
        # 1. detect if there is if/else/for/while 2. if true, find if there is { in the next sentence
        # 3. if true, skip; if false, recursive..
        def detect_keywords(self, index):
            if self.reg_if.match(self.text[index]) or \
               self.reg_else.match(self.text[index]) or \
               self.reg_for.match(self.text[index]) or \
               self.reg_while.match(self.text[index]) or \
               self.reg_elseif.match(self.text[index]):
                if self.text[index+1].find('{') != -1:
                    return index+2
                else:
                    self.left_brace[index] = 1
                    self.left_brace_accumulate += 1
                    if self.reg_if.match(self.text[index+1]) or \
                       self.reg_else.match(self.text[index+1]) or \
                       self.reg_for.match(self.text[index+1]) or \
                       self.reg_while.match(self.text[index+1]) or \
                       self.reg_elseif.match(self.text[index+1]):
                        return self.detect_keywords(index+1)
                    else:
                        self.right_brace[index+1] = self.left_brace_accumulate
                        self.left_brace_accumulate = 0
                        return index+2
            else:
                return index+1

        # 4.1.1.5
        # detect the if/else/while/for brace for the whole text
        def add_brace(self):
            # Detect brace
            index = 0
            while index < len(self.text):
                index = self.detect_keywords(index)

            # Add brace
            all_pos = list(self.right_brace.keys()) + list(self.left_brace.keys())
            all_pos.sort(reverse=True)
            for element in all_pos:
                if self.left_brace.has_key(element):
                    self.text[element:element+1] = self.text[element:element+1] + ['{'] * self.left_brace[element]
                if self.right_brace.has_key(element):
                    self.text[element:element+1] = self.text[element:element+1] + ['}'] * self.right_brace[element]

        # 4.1.1.8, all the left braces occupy a new line
        def left_brace_new_line(self):
            index = 0
            reg_left_brace = re.compile(r'([\s\S]+)(\{)([\s\S]*)')
            while index < len(self.text):
                match = reg_left_brace.match(self.text[index])
                if match:
                    index = list_replace(self.text, index, word_clean(match.groups()))
                else:
                    index += 1

        # 4.1.1.3 correct all the indent
        def indent_adjustment(self):
            index_level = 0;
            for i in range(len(self.text)):
                self.text[i] = ' '*int(self.tabstop*index_level) + self.text[i].strip()
                if self.text[i].find('{') != -1:
                    index_level += 1
                if self.text[i].find('}') != -1:
                    index_level -= 1
                    self.text[i] = ' '*int(self.tabstop*index_level) + self.text[i].strip()
                    if index_level < 0:
                        raise SystaxError("Syntax Error in line({})".format(i))

        # 4.1.3
        # In this part, two things are important:
        # 1. to identify that something is a function
        # 2. to identify what function the calling happens in
        def identify_function_names(self):
            reg_function = re.compile(r'[\s\S]*?\s*?(\w+)\([\s\S]*?\)\s*')
            reg_struct = re.compile(r'struct\s+?(\w+)\s*')
            reg_typedef = re.compile(r'typedef\s+?(\w+)\s+?(\w+)\s*')
            for line in self.text:
                if reg_struct.match(line):
                    self.exclude_words = self.exclude_words + word_clean(reg_struct.match(line).groups())
                elif reg_typedef.match(line):
                    self.exclude_words = self.exclude_words + word_clean(reg_typedef.match(line).groups())
                elif reg_function.match(line):
                    word = word_clean(reg_function.match(line).groups())[0]
                    if word not in self.exclude_words:
                        self.functions.append(word)
            self.functions = list(set(self.functions))
            self.exclude_words = list(set(self.exclude_words))

        def identify_function_calling(self):
            reg_function = re.compile(r'[\s\S]*?\s*?(\w+)\([\s\S]*\)[\s\S]*')
            reg_function_list = [
                re.compile(r'[\s\S]*?\s+?(' + x.strip() + ')\([\s\S]*\)[\s\S]*') for x in self.functions
            ]
            reg_function_define = re.compile(r'\s*(\w+)\s+(\w+)\([\s\S]*?\)\s*')
            zone = None
            for line in self.text:
                if reg_function_define.match(line):
                    declaration = word_clean(reg_function_define.match(line).groups())
                    if declaration[1] in self.functions:
                        zone = declaration[1]
                    else:
                        if not declaration[1] in self.exclude_words:
                            sys.stderr.write('Function Declaration not found.\n' +
                                             '{} {}\n'.format(declaration[0], declaration[1]) +
                                             'in line({})'.format(self.text.index(line)))
                elif reg_function.match(line):
                    for reg_element in reg_function_list:
                        if reg_element.match(line):
                            function_name = word_clean(reg_element.match(line).groups())[0]
                            if zone in self.calling_relationship:
                                self.calling_relationship[zone].append(function_name)
                            else:
                                self.calling_relationship[zone] = [function_name]
                            if function_name in self.called_relationship:
                                self.called_relationship[function_name].append(zone)
                            else:
                                self.called_relationship[function_name] = [zone]
            for key in self.called_relationship:
                self.called_relationship[key] = list(set(self.called_relationship[key]))
            for key in self.calling_relationship:
                self.calling_relationship[key] = list(set(self.calling_relationship[key]))

        # output for the calling relationships
        def generate_calling_relationship_output(self):
            result = []
            self.functions.sort()
            for func in self.functions:
                func_dict = {'FunctionName':func}
                if func in self.called_relationship:
                    self.called_relationship[func].sort()
                    func_dict['Caller'] = ','.join(self.called_relationship[func])
                else:
                    func_dict['Caller'] = ''
                if func in self.calling_relationship:
                    self.calling_relationship[func].sort()
                    func_dict['Called'] = ','.join(self.calling_relationship[func])
                else:
                    func_dict['Called'] = ''
                if func_dict['Called'] is not '' or func_dict['Caller'] is not '':
                    result.append(func_dict)
            self.result = result

        def output_to_file(self):
            s = ''
            for element in self.result:
                s = s + "FunctionName:{}\nCaller:{}\nCalled:{}\n\n".format(element['FunctionName'], element['Caller'], element['Called'])
            return s


        # 4.1.1.6
        # Delete the vacuum using the regex pattern ^\s*;\s*$ and ^\s*$
        def delete_vacuum(self):
            # Detect vacuum lines
            reg_vacuum_line = re.compile(r'^\s*;\s*$')
            reg_empty = re.compile(r'^\s*$')
            for i in range(len(self.text)):
                if reg_vacuum_line.match(self.text[i]) or reg_empty.match(self.text[i]):
                    self.vacuum_lines.append(i)

            # Detele them
            self.vacuum_lines.sort(reverse=True)
            for i in self.vacuum_lines:
                del self.text[i]

    # According to the style, choose the required function
    def run_by_rule(self):

        # Delete Comment
        self.comment_delete()
        # Calculate Lines
        self.lines = len(list(filter(lambda x: x.find('<empty>') == -1,self.text)))

        # Unify the format
        for i in range(len(self.text)):
            line = self.text[i]
            # 4.1.1.1 first condition
            if self.style['function']['left_parenthesis_blank'] == False:
                line = LexicalMachine.function_left_parenthesis_blank(line)
            # 4.1.1.1 second condition
            if self.style['function']['left_parenthesis_newline'] == False and \
                i+1 < len(self.text):
                line, self.text[i+1] = LexicalMachine.function_left_parenthesis_newline(line, self.text[i+1])

            # 4.1.1.2
            # if self.style['parenthesis']['left_parenthesis_right_blank'] == False and \
            #    self.style['parenthesis']['right_parenthesis_left_blank'] == False:
            #     line = LexicalMachine.parenthesis_blank(line)
            #     if i+1 < len(self.text):
            #         line, self.text[i+1] = LexicalMachine.parenthesis_new_line(line, self.text[i+1])

            # 4.1.1.2
            if self.style['parenthesis']['left_parenthesis_right_blank'] == False:
                line = LexicalMachine.left_right_parenthesis_blank(line)
                # if i+1 < len(self.text):
                    # line, self.text[i+1] = LexicalMachine.parenthesis_new_line(line, self.text[i+1])

            if self.style['parenthesis']['right_parenthesis_left_blank'] == False:
                line = LexicalMachine.right_left_parenthesis_blank(line)
                # if i+1 < len(self.text):
                #     line, self.text[i+1] = LexicalMachine.parenthesis_new_line(line, self.text[i+1])

            if self.style['parenthesis']['left_parenthesis_right_blank'] == False and \
               self.style['parenthesis']['right_parenthesis_left_blank'] == False:
                if i+1 < len(self.text):
                    line, self.text[i+1] = LexicalMachine.parenthesis_new_line(line, self.text[i+1])

            # 4.1.1.4
            line = self.special_character_blank(line)
            self.text[i] = line

        # 4.1.1.7
        if self.style['one_statement_per_line'] == True:
            self.multiple_code_split_and_replace()

        self.global_machine = self.GlobalCharacterAnalysis(self.text, self.style['tabstop'])
        # 4.1.1.8
        if self.style['brace']['left_brace_new_line'] == True:
            self.global_machine.left_brace_new_line()
        # 4.1.1.5
        if self.style['brace']['brace_for_block'] == True:
            self.global_machine.add_brace()
        # 4.1.1.3
        self.global_machine.indent_adjustment()
        # 4.1.1.6
        if self.style['delete_empty_statement'] == True:
            self.global_machine.delete_vacuum()

        # Generate calling relationships
        self.global_machine.identify_function_names()
        self.global_machine.identify_function_calling()
        self.global_machine.generate_calling_relationship_output()

    def output_to_file(self):
        self.text = list(map(lambda x: '' if x.find('<empty>') != -1 else x, self.text))
        with open(self.output_filename,'w') as f:
            f.write('\n'.join(self.text))
        with open(self.output_info, 'w') as f:
            f.write('Lines:{}\n\n'.format(self.lines))
            self.info = 'Lines:{}\n\n'.format(self.lines)

            s = self.global_machine.output_to_file()
            self.info += s
            f.write(s)

    def run(self):

        self.lines = 0
        self.info = ''
        self.text = []
        self.style = {}

        # Open source file by source_filename
        try:
            self.source_file = open(self.source_filename)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            exit(0)

        # Read source code and handle it, save to self.text
        self.read_source_code(self.source_file)
        self.source_file.close()

        # Open style file by style_filename
        # Read style file
        # Check style file
        try:
            if self.style_filename:
                self.style_file = open(self.style_filename)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror) +
                  "Using default style instead")
        else:
            if self.style_file:
                self.read_style(self.style_file)
                self.style_file.close()
        finally:
            self.style_check()
            # for key, value in self.style.items():
            #     print key, ':',  value


        self.run_by_rule()
        self.output_to_file()

        # for index,item in enumerate(self.text):
        #     print item

if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '-style':
        style_filename = sys.argv[2]
        source_filename = sys.argv[3]
    elif len(sys.argv) == 3 and sys.argv[1].startswith("--style=") and len(sys.argv[1]) > 8:
        style_filename = sys.argv[1][8:]
        source_filename = sys.argv[2]
    elif len(sys.argv) == 2:
        style_filename = None
        source_filename = sys.argv[1]
    else:
        print("The usage of the program is \n" +
              "\t{} -style <style file> <source code> \n".format(sys.argv[0]) +
              "\t{} -style==<style file> <source code> \n".format(sys.argv[0]) +
              "\t{} <source code> \n".format(sys.argv[0]))
        exit(0)
    lecical_machine = LexicalMachine(source_filename, style_filename)
    lecical_machine.run()
