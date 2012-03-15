#!/usr/bin/python

from sys import argv
from sys import exit
import re

file = list(open(argv[1],'r'))
out = open("out.tex",'w')

def tail(s): return s[1:]
def init(s): return s[:len(s)-1]
def last(s): return s[len(s)-1]
def head(s): return s[0]
def clean(s,c):
    while s.count(c) != 0: s = s.replace(c,"")
    return s
def cleanstart(s,c):
    if s == "": return s
    while s[0] == c:
        s = tail(s)
    return s
def cleanend(s,c):
    if s == "": return s
    while s[len(s)-1] == c:
        s = init(s)
    return s
def cleanends(s,c):
    return cleanstart(cleanend(s,c),c)
def pareneq(s):
    depth = 0
    for c in s:
        if c in "([{": depth += 1
        if c in ")]}": depth -= 1
        if depth < 0:
            return False
    return depth == 0
def parts(s,clist):
    result = ""
    for c in s:
        if c in clist and pareneq(result):
            return (result,s[len(result):])
        else:
            result += c
    return (None,s)


regex = [
    ('((.{,1}\(.*\))|([^ ]*)) *\/',"DIVISION"),
    ('\(.*\)',"PARENS"),
    ('\+.*',"+"),
    ('-.*',"-"),
    ('\*.*',"*"),
    ('_.*',"SUBSCRIPT"),
    ('\^.*',"SUPERSCRIPT"),
    ('=.*',"="),
    ('forall',"\\forall"),
    ('dot',"\\cdot"),
    ('xhat',"\\hat{x}"),
    ('yhat',"\\hat{y}"),
    ('zhat',"\\hat{z}"),
    ('rhat',"\\hat{r}"),
    ('phihat',"\\hat{\\phi}"),
    ('thetahat',"\\hat{\\theta}"),
    ('xdot',"\\dot{x}"),
    ('ydot',"\\dot{y}"),
    ('zdot',"\\dot{z}"),
    ('rdot',"\\dot{r}"),
    ('phidot',"\\dot{\\phi}"),
    ('thetadot',"\\dot{\\theta}"),
    ('rddot',"\\ddot{r}"),
    ('phiddot',"\\ddot{\\phi}"),
    ('thetaddot',"\\ddot{\\theta}"),
    ('xddot',"\\ddot{x}"),
    ('yddot',"\\ddot{y}"),
    ('zddot',"\\ddot{z}"),
    ('alpha',"\\alpha"),
    ('beta',"\\beta"),
    ('gamma',"\\gamma"),
    ('delta',"\\delta"),
    ('epsilon',"\\epsilon"),
    ('zeta',"\\zeta"),
    ('eta',"\\eta"),
    ('theta',"\\theta"),
    ('iota',"\\iota"),
    ('kappa',"\\kappa"),
    ('lambda',"\\lambda"),
    ('mu',"\\mu"),
    ('nu',"\\nu"),
    ('xi',"\\xi"),
    ('omicron',"\\omicron"),
    ('pi',"\\pi"),
    ('rho',"\\rho"),
    ('sigma',"\\sigma"),
    ('tau',"\\tau"),
    ('upsilon',"\\upsilon"),
    ('phi',"\\phi"),
    ('chi',"\\chi"),
    ('psi',"\\psi"),
    ('omega',"\\omega"),
    ('Gamma',"\\Gamma"),
    ('Delta',"\\Delta"),
    ('Theta',"\\Theta"),
    ('Lambda',"\\Lambda"),
    ('Xi',"\\Xi"),
    ('Pi',"\\Pi"),
    ('Sigma',"\\Sigma"),
    ('Upsilon',"\\Upsilon"),
    ('Phi',"\\Phi"),
    ('Psi',"\\Psi"),
    ('Omega',"\\Omega")
]

def rmatch(s):
    for r in regex:
        token = re.compile(r[0]).match(s)
        if token and pareneq(token.group()):
            return (r[1],token.group())
    return ("NONE",parts(s," ()^*+-_"))
def parse(s):
    m = rmatch(s)
#    print m
    checkdiv = parts(s," /")
    chd0 = checkdiv[0]
    chd1 = cleanstart(checkdiv[1]," ")
    if m[0] == "NONE":
        if not m[1][0]:
            return s
        else:
            return m[1][0] + parse(cleanstart(m[1][1]," "))
    elif chd1[0] == "/":
        num = chd0
        rem = cleanstart(tail(chd1)," ")
        splitrem = parts(rem," *+-")
        den = splitrem[0]
        end = cleanstart(splitrem[1]," ")
        if not splitrem[0]:
            den = splitrem[1]
            end = ""
        return "\\frac{" + parse(num) + "}{" + parse(den) + "}" + parse(end)
    elif m[0] == "PARENS":
        return "(" + parse(cleanends(init(tail(m[1]))," ")) + ")" + parse(cleanstart(s[len(m[1]):]," "))
    elif m[0] == "+":
        return "+" + parse(cleanstart(tail(m[1])," "))
    elif m[0] == "-":
        return "-" + parse(cleanstart(tail(m[1])," "))
    elif m[0] == "*":
        return "*" + parse(cleanstart(tail(m[1])," "))
    elif m[0] == "=":
        return "=" + parse(cleanstart(tail(m[1])," "))
    elif m[0] == "SUBSCRIPT":
        sep = parts(tail(m[1])," ^*+-")
        if not sep[0]: return "_{" + sep[1] + "}"
        return "_{" + parse(sep[0])  + "}" + parse(cleanstart(sep[1]," "))
    elif m[0] == "SUPERSCRIPT":
        sep = parts(tail(m[1])," ^*+-")
        if not sep[0]: return "^{" + sep[1] + "}"
        return "^{" + parse(sep[0])  + "}" + parse(cleanstart(sep[1]," "))
    else:
        return m[0] + " " + parse(cleanstart(s[len(m[1]):]," "))

def splitdef(s,q):
    d = init(tail(s))
    loc = d.find(q)
    return (d[:loc],d[loc+4:]+" ")

out.write("\\documentclass[11pt]{article}\n")
out.write("\\linespread{1.5}\n")
out.write("\\usepackage{amsmath}\n")
out.write("\\usepackage[margin=1in]{geometry}\n")
out.write("\\begin{document}\n")
for l in file:
    if l[0] == "\n":
        continue
    if l[0] == " ":
        line = tail(l).replace("\n"," ") + " "
        if re.compile('       [^ ]').match(line):
            out.write("\\begin{center} \\large \\textsc{" + cleanstart(line," ") + "} \\normalsize \\end{center}\n\n")
            continue
        elif re.compile('     [^ ]').match(line):
            out.write("\\begin{center}" + cleanstart(line," ") + " \\end{center}\n\n")
            continue
        elif re.compile('   [^ ]').match(line):
            out.write("\\vspace{10mm} \\Large \\textbf{" + cleanstart(line," ") + "} \\normalsize\n\n")
            continue
        elif re.compile(' [^ ]').match(line):
            out.write("\\large \\textbf{" + cleanstart(line," ") + "} \\normalsize\n")
            continue
        result = ""
        mathbuf = ""
        mathmode = False
        while not line == "":
            math = re.compile('  ((?!  ).)*(  |\.)').match(line)
            if math:
                mathgroup = math.group()
                result += " $" + parse(mathgroup.replace("  ","")) + "$ "
                line = line[len(mathgroup):]
            else:
                result += line[0]
                line = tail(line)
        out.write(result + "\n\n")
    elif l[0] == "\\":
        regex = [splitdef(l," == ")] + regex
    else:
        l = cleanend(l,"\n")
        if not pareneq(l):
            print "Error on line", file.index(l), "in file", argv[1]
            exit()
        out.write("$" + parse(l) + "$\n\n")
out.write("\\end{document}")

out.close()
