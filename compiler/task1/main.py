#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：main.py 
@File    ：main.py
@Author  ：Polaris
@Date    ：2022-05-25 11:01
'''
import re

keyword = ['auto', 'break', 'case', 'char', 'const',
           'continue', 'default', 'do', 'double', 'else', 'enum',
           'extern', 'float', 'for', 'goto', 'if', 'int', 'long',
           'register', 'return', 'short', 'signed', 'sizeof', 'static',
           'struct', 'switch', 'typedef', 'union', 'unsigned', 'void'
    , 'volatile', 'while']
operator = ['+', '-', '*', '/', '%', '++', '--', '+=', '-=', '+=', '/=',  # 算术运算符
            '==', '!=', '>', '<', '>=', '<=',  # 关系运算符
            '&', '|', '^', '~', '<<', '>>',  # 位运算符
            '&&', '||', '!',  # 逻辑运算符
            '=',  # 赋值运算符
            ]
delimiters = ['{', '}', '[', ']', '(', ')', '.', ',', ':', ';']


def isIdentifier(str):
    if len(str) == 1:
        return str[0] == '_' or str[0].encode().isalpha()
    else:
        return (str[0] == '_' or str[0].isalpha()) and str[1:].replace('_', '').encode().isalnum()
    # 不加.encode()没法识别中文


# str.isdigit()
# str.isalpha()
# 处理注释'//''/*''*/'
def isKeywords(str):
    if str in keyword:
        return True
    else:
        return False


if __name__ == '__main__':
    identifier = []
    token = []
    filename = input("filename:")
    fp = open(filename, encoding='utf-8', mode='r')
    txt = fp.read()
    lines = re.sub(r'\/\*[\s\S]*\*\/|\/\/.*', '', txt).split('\n')  # 用正则表达式去掉注释
    # ori_lines=fp.readlines()
    fp.close()
    # lines_list=[line.strip('\n').replace('\\t','').split(' ') for line in lines]    #按空格分割字符串
    lines = [line.strip('\n').replace('\t', '') for line in lines]
    identifier = []
    flag = False  # 当遇见两位的运算符时，通过flag跳过下一个字符
    for line in lines:
        word = ''
        if line == '':
            continue
            # 空字符串跳过,进入下一行
        else:
            # for ch in line:
            i = -1
            while (i + 1 < len(line)):
                i = i + 1
                ch = line[i]
                if ch == ' ':
                    continue
                # 分界符：
                if ch in delimiters:
                    token.append(f'<delimiter,{delimiters.index(ch)},\'{ch}\'>')
                # 运算符：
                elif ch in operator:
                    next = line[i:i + 2]
                    if next in operator:
                        token.append(f'<operator,{operator.index(next)},\'{next}\'>')
                        i = i + 1  # 跳过下一个循环
                    else:
                        token.append(f'<operator,{operator.index(ch)},\'{ch}\'>')
                # 数字：
                elif ch.isnumeric():
                    base = 10  # 默认十进制
                    num = ch
                    if ch == '0' and i + 1 < len(line) and line[i + 1] in 'xboXBO':
                        if i + 1 < len(line) and (line[i + 1] == 'x' or line[i + 1] == 'X'):
                            num = '0x'
                            base = 16
                            i = i + 1
                        elif i + 1 < len(line) and (line[i + 1] == 'o' or line[i + 1] == 'O'):
                            num = '0o'
                            base = 8
                            i = i + 1
                        elif i + 1 < len(line) and (line[i + 1] == 'b' or line[i + 1] == 'B'):
                            num = '0b'
                            base = 2
                            i = i + 1
                    while i + 1 < len(line) and (line[i + 1] in '0123456789abcdefABCDEF'):
                        num = num + line[i + 1]
                        i = i + 1
                    else:
                        if not num in '0x0o0b':
                            token.append(f'<num,{int(num, base)}>')
                # 标识符/关键词：
                elif isIdentifier(ch):
                    word = ch
                    while (i + 1 < len(line) and isIdentifier(line[i + 1])):
                        word = word + line[i + 1]
                        i = i + 1
                    else:
                        if word in keyword:
                            token.append(f'<{word}>')
                            word = ''
                        else:
                            if not word in identifier:
                                identifier.append(word)
                            token.append(f'<identifier,{identifier.index(word)},\'{word}\'>')
                            word = ''
                else:
                    print(f'Error at line {lines.index(line) + 1}:不允许的字符')
                    continue
    for i, x in enumerate(token):
        print(x)
