#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：main.py 
@File    ：main.py
@Author  ：Polaris
@Date    ：2022-05-25 13:31
'''
# 文法
dict = {
    "E": ["TG"],
    "G": ["ATG", 'ε'],
    "T": ["FH"],
    "H": ["MFH", 'ε'],
    "F": ["(E)", "i"],
    "A": ["+", "-"],
    "M": ["*", "/"]
}
# 文法右部
# 文法
# dict = {
#     "S": ['aAB', 'd'],
#     "A": ['bAS', 'ε'],
#     "B": ['cAB', 'ε']
# }
# 文法右部
Vr = []
for item in dict.keys():
    Vr.extend(dict[item]);
Vr = list(set(Vr))
Vr.sort()
# 非终结符
VN = []
for item in dict.keys():
    VN.append(item);
print("非终结符VN集合为：{}".format(VN))

# 终结符
VT = []
for item in dict.values():
    for it in item:  # 遍历key值
        for i in it:
            if i not in VN and i != "'":
                VT.append(i)
VT = list(set(VT))
# 排序
VT.sort()
# VT.append("ε")
print("终结符VT集合为:{}".format(VT))


# 翻转字符串，返回字符串
def Reverse(str):
    return str[::-1]


# 找产生式,返回产生式右部
def findR(Vn, str0):
    if Vn in dict.keys():
        ProRight = dict[Vn]
        for str in ProRight:
            if str0 == str[0]:
                return str
    return ''


def findL(item):
    for SL in VN:
        for it in dict[SL]:
            if it == item:
                return SL
    return ''


# 将产生式添加进栈内
def addS(V, S):
    newS = list(S)
    for i in V:
        newS.append(i)
    return newS


# 获取 First集
def Fi(S):
    if S in VN:
        Fi = []
        return First(S, Fi)
    else:
        return list(S)


def First(S, Fi):
    if S in VT:
        Fi.append(S)
    for item in dict[S]:
        if item[0] in VT:
            Fi.append(item[0])
        else:
            First(item[0], Fi)
    Fi = list(set(Fi))
    Fi.sort()
    return Fi


# print(Fi('B'))

# 获取 Follow 集
def Fo(S):
    if S in VN:
        Fo = []
        Fo = Follow(S, Fo)
        Fo = list(set(Fo))
        Fo.sort()
        if 'ε' in Fo:
            Fo.remove('ε')
        return Fo
    else:
        return list(S)


def Follow(S, Fo):
    if S == VN[0]:
        Fo.append('$')
    for item in Vr:
        if S in item:
            i = item.index(S)
            if i + 1 < len(item):
                # aBc
                if item[i + 1] in VT:
                    Fo.append(item[i + 1])
                # A->aBC
                elif item[i + 1] in VN:
                    First(item[i + 1], Fo)
                    # C->ε
                    if findR(item[i + 1], 'ε') != '' and findL(item) != item[len(item) - 1]:
                        Follow(findL(item), Fo)
            # aB
            else:
                if findL(item) != item[len(item) - 1]:
                    Follow(findL(item), Fo)
                else:
                    pass

    return Fo


# 获取 Select 集
def Se(S, V):
    if S in VN:
        Se = []
        return Select(S, V, Se)


def Select(S, V, Se):
    if V[0] in VT and V[0] != 'ε':
        return list(V[0])
    elif V[0] == 'ε':
        Se.extend(Fo(S))
        return Se
    elif V[0] in VN:
        if 'ε' in dict[V[0]]:
            Se.extend(V[1])
            Se.remove('ε')
            Se.extend(Fo(V[0]))
        Se.extend(Fi(V[0]))
        return Se
    return Se


# 分析表
VTn = []
VTn = VT[:]
dicM = {vn: {} for vn in VN}
VTn.remove('ε')
VTn.append('$')
print('分析表：')
print("  ", end='')
print(''.join(str(i).center(5) for i in VTn))
for S in VN:
    li = []
    for i in range(len(VT)):
        li.append('err')
    print(S, end=' ')
    for Si in dict[S]:
        for item in VTn:
            if item in Se(S, Si):
                i = VTn.index(item)
                li[i] = Si
    print(''.join(str(i).center(5) for i in li))
    for ind, i in enumerate(li):
        if i != 'err':
            dicM[S][VTn[ind]] = i
    print('\n')


# 翻转字符串，返回字符串
def convertStr(arg):
    revstr = ""
    i = len(arg)
    while i > 0:
        if arg[i - 1] != "'":
            revstr += arg[i - 1]
        else:
            revstr += arg[i - 2]
            revstr += arg[i - 1]
            i -= 1
        i -= 1
    return revstr


# 找产生式,返回产生式右部
def findCSS(argS, argstr):
    if argS in dicM.keys():
        temp_value = dicM[argS]
        if argstr in temp_value.keys():
            temp = temp_value[argstr]
            return temp
    return ""


# 截取列表 除去最后一个元素
def substr(arg):
    # print(arg,"fdsfs")
    Listarg = list(arg)
    le = len(Listarg)
    args = Listarg[0:le - 1]
    return args


def addS(arg, args):
    Listargs = list(args)
    for i in arg:
        Listargs.append(i)
    return Listargs


# strString=input("请输入要分析的符号串：")#输入串
strString = input("输入符号串：")
str = list(strString)
str.append("$")
COUNT = 0  # 步骤
# 符号栈
S = ["$"]
S.append(VN[0])
# print(S)
CSRight = ""
print("步骤\t符号栈S[i]\t输入串str[j]\t产生式")
while len(S) != 0:
    COUNT += 1
    ch = str[0]
    CSRight0 = findCSS(S[-1], str[0])
    if CSRight0 != "" and S[-1] not in VT:
        print("%s\t%s\t%s\t%s" % (COUNT, "".join(S).center(10), "".join(str).center(10), S[-1] + "->" + CSRight0))
    elif CSRight0 in VT or S[-1] in VT:
        print("%s\t%s\t%s\t匹配弹出%s" % (COUNT, "".join(S).center(10), "".join(str).center(10),str[0]))
    elif CSRight0 == "":
        print("\033[0;31m%s\033[0m" % "该句子不是该文法！")
        break
    CHS = S.pop()
    CSRight = findCSS(CHS, str[0])
    if CHS not in VT:  # 如果栈顶元素不是终结字符
        if CSRight != "":
            if CSRight[0] in VN:
                temp = convertStr(CSRight)
                S = addS(temp, S)
            elif CSRight[0] in VT and CSRight[0] != "ε":
                temp = convertStr(CSRight)
                S = addS(temp, S)
            elif CSRight[0] == "ε" and CSRight[0] in VT:
                if S == ["$"]:
                    if str[0] == "$":
                        # print("该句子属于该文法！")
                        print("\033[1;31;40m该句子属于该文法！\033[0m")
                        break
        elif CSRight == "":
            pass
    elif CHS in VT:
        if ch == CHS:
            if CHS == "$":
                # print("该句子属于该文法！")
                print("\033[1;31;40m该句子属于该文法！\033[0m")
            elif CHS != "$":
                str = str[1:]
        elif ch != CHS:
            if CHS == "$":
                print("\033[0;31m%s\033[0m" % "该句子不是该文法！")
                pass
