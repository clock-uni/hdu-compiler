#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：main.py 
@File    ：main.py
@Author  ：Polaris
@Date    ：2022-05-25 11:17
'''


class Diguixiajiang():  # 递归下降
    def __init__(self):
        self.ans = ""
        self.index = 0;  # 遍历字符串的当前位置
        self.str = ""
        self.flag = 0

    def getString(self, string):
        self.str = string
        return self.str

    def E(self, t):
        if t == '(':
            print("E::TE'")
            self.ans = self.ans + "E::TE'\n"
            self.T(self.str[self.index])
            self.Ep(self.str[self.index])

        elif t == 'i':
            print("E::TE'")
            self.ans = self.ans + "E::TE'\n"
            self.T(self.str[self.index])
            self.Ep(self.str[self.index])

        else:
            self.error();
            self.index += 1
            self.E(self.str[self.index])

    def T(self, t):
        if t == 'i':
            print("T::FT'")
            self.ans = self.ans + "T::FT'" + "\n"
            self.F(self.str[self.index])
            self.Tp(self.str[self.index])

        elif t == '(':
            print("T::FT'")
            self.ans = self.ans + "T::FT'" + "\n"
            self.F(self.str[self.index])
            self.Tp(self.str[self.index])
        else:
            self.error()
            self.index += 1
            self.T(self.str[self.index])

    def Ep(self, t):
        if t == ')':
            print("E'::ε")
            self.ans = self.ans + "E'::ε" + "\n"
            self.index += 1
        elif t == '+':
            print("E'::ATE'")
            self.ans = self.ans + "E'::ATE'" + "\n"
            self.A(self.str[self.index]);
            self.T(self.str[self.index]);
            self.Ep(self.str[self.index]);
        elif t == '-':
            print("E'::ATE'")
            self.ans = self.ans + "E'::ATE'" + "\n"
            self.A(self.str[self.index]);
            self.T(self.str[self.index]);
            self.Ep(self.str[self.index]);
        elif t == '$':
            print("E'::ε")
            self.ans = self.ans + "E'::ε" + "\n"
        else:
            self.error()
            self.index += 1
            self.Ep(self.str[self.index]);

    def Tp(self, t):
        if t == ')':
            print("T'::ε")
            self.ans = self.ans + "T'::ε" + "\n"
        elif t == '+':
            print("T'::ε")
            self.ans = self.ans + "T'::ε" + "\n"
        elif t == '-':
            print("T'::ε")
            self.ans = self.ans + "T'::ε" + "\n"
        elif t == '*':
            print("T'::MFT'")
            self.ans = self.ans + "T'::MFT'" + "\n"
            self.M(self.str[self.index])
            self.F(self.str[self.index])
            self.Tp(self.str[self.index])
        elif t == '/':
            print("T'::MFT'")
            self.ans = self.ans + "T'::MFT'" + "\n"
            self.M(self.str[self.index])
            self.F(self.str[self.index])
            self.Tp(self.str[self.index])
        elif t == '$':
            print("T'::ε")
            self.ans = self.ans + "T'::ε" + "\n"
        else:
            self.error()
            self.index += 1
            self.Tp(self.str[self.index]);

    def F(self, t):
        if t == 'i':
            print("F::i")
            self.ans = self.ans + "F::i" + "\n"
            self.index += 1;
        elif t == '(':
            print("F->(E)")
            self.ans = self.ans + "F->(E)" + "\n"
            self.index += 1;
            self.E(self.str[self.index]);

        else:
            self.error()
            self.index += 1
            self.F(self.str[self.index]);

    def A(self, t):
        if t == '+':
            print("A::+")
            self.ans = self.ans + "A::+" + "\n"
            self.index += 1
        elif t == '-':
            print("A::-")
            self.ans = self.ans + "A::-" + "\n"
            self.index += 1
        else:
            self.error()
            self.index += 1
            self.A(self.str[self.index]);

    def M(self, t):
        if t == '*':
            print("M::*")
            self.ans = self.ans + "M::*" + "\n"
            self.index += 1
        elif t == '/':
            print("M::/")
            self.ans = self.ans + "M::/" + "\n"
            self.index += 1
        else:
            self.error()
            self.index += 1
            self.M(self.str[self.index]);

    def error(self):
        print("有一个错误，略过当前词法记号")
        self.flag = 1;


if __name__ == '__main__':
    file = input('filename:')
    file2 = r"D:\TOOL\jupyter program\compiler\task2\out.txt"
    with open(file, 'r', encoding='utf-8') as f:
        for ind, s in enumerate(f):
            string = ""
            if s == '':
                continue
            print('处理第', ind + 1, '条指令中', sep='')
            string += s
            xj = Diguixiajiang()
            str = xj.getString(string)
            print(str)
            # System.out.println(str.charAt(1));

            xj.E(str[xj.index])
            print("语法分析完成")
            if xj.flag == 1:
                print("当前语句不合法")
            else:
                print("当前语句合法")
