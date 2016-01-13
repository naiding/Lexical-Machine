__author__ = 'zhounaiding'

from Lexical_machine import LexicalMachine


def file_diff(filename1, filename2):
    print("Start Comparing:\n\tfile-1:{}\n\tfile-2:{}".format(filename1, filename2))
    with open(filename1, 'r') as f:
        text1 = f.readlines()
    with open(filename2, 'r') as f:
        text2 = f.readlines()
    text1 = list(map(lambda x: x.strip(), text1))
    text2 = list(map(lambda x: x.strip(), text2))
    status = True
    if len(text1) != len(text2):
        if len(text1) < len(text2):
            for i in range(len(text1)):
                if text1[i] != text2[i]:
                    status = False
                    print("Line:{}\n->{}\n<-{}".format(i, text1[i], text2[i]))
        else:
            for i in range(len(text2)):
                if text1[i] != text2[i]:
                    status = False
                    print("Line:{}\n->{}\n<-{}".format(i, text1[i], text2[i]))
    else:
        for i in range(len(text1)):
                if text1[i] != text2[i]:
                    status = False
                    print("Line:{}\n->{}\n<-{}".format(i, text1[i], text2[i]))
    print("----------\n")

if __name__ == '__main__':

    file_path = '/Users/zhounaiding/Desktop/lexical/test/codeE1.c'
    # file_output_path = '/Users/zhounaiding/Desktop/lexical/test/codeE1_output.c'
    style_file_path = '/Users/zhounaiding/PycharmProjects/Python/Lexical-Machine-master/default.style'
    # original_file = '/Users/zhounaiding/Desktop/lexical/test/code.c'

    lexical = LexicalMachine(file_path, style_file_path)
    lexical.run()
    # file_diff(files_output, original_file)

    # files_with_error_list = ['/Users/zhounaiding/PycharmProjects/Python/Lexical-Machine/test/codeE{}.c'.format(x) for x in range(1,9)]
    # files_output = ['/Users/zhounaiding/PycharmProjects/Python/Lexical-Machine/test/codeE{}_output.c'.format(x) for x in range(1,9)]
    # original_file = '/Users/zhounaiding/PycharmProjects/Python/Lexical-Machine/test/code.c'

    # files_with_error_list = ['./test/codeE{}.c'.format(x) for x in range(1,9)]
    # files_output = ['./test/codeE{}_output.c'.format(x) for x in range(1,9)]
    # original_file = './test/code.c'
    # for filename in files_with_error_list:
    #     lexical = LexicalMachine(filename, None)
    #     lexical.run()
    # for i in range(8):
    #     file_diff(files_output[i], original_file)

