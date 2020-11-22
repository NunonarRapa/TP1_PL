import ply.lex as lex
import re
import sys
import webbrowser
from utils import readFile

if len(sys.argv) != 2:
    print("Pass the filename to analyze")
    exit(1)
else:
    filename = sys.argv[1]


testcomment = r"[ ]-[ ].*\n"


testpos = rf"ok[ ][0-9]+(\n|{testcomment})"


testneg = rf"not[ ]ok[ ][0-9]+(\n|{testcomment})"


subtestpos = rf"[ ]+{testpos}"


subtestneg = rf"[ ]+{testneg}"


tokens = ("TESTPLAN", "TESTPOS", "TESTNEG", "COMMENT", "SUBTESTPOS", "SUBTESTNEG")


@lex.TOKEN(testpos)
def t_TESTPOS(t):
    return t


@lex.TOKEN(testneg)
def t_TESTNEG(t):
    return t


@lex.TOKEN(subtestpos)
def t_SUBTESTPOS(t):
    return t


@lex.TOKEN(subtestneg)
def t_SUBTESTNEG(t):
    return t


def t_TESTPLAN(t):
    r"[ ]*[0-9]\.\.[0-9]+.*\n"
    return t


def t_COMMENT(t):
    r"[ ]*\#.*\n"
    pass


def t_error(t):
    print("Unexpected string: %s" % t.value)
    exit(1)


lexer = lex.lex()
lexer.input(readFile(filename))

poscount = 0
negcount = 0
subposcount = 0
subnegcount = 0
postests = []
negtests = []

for token in iter(lexer.token, None):
    if token.type == "TESTPOS":
        captures = re.fullmatch(rf"ok[ ]([0-9]+)(\n|{testcomment})", token.value)
        postests.append((captures.group(1)))
        poscount += 1
    if token.type == "TESTNEG":
        captures = re.fullmatch(rf"not[ ]ok[ ]([0-9]+)(\n|{testcomment})", token.value)
        negtests.append((captures.group(1)))
        negcount += 1
    if token.type == "SUBTESTPOS":
        subposcount += 1
    if token.type == "SUBTESTNEG":
        subnegcount += 1

totaltests = poscount + negcount
totalsubtests = subposcount + subnegcount

f = open("main.html", "w")
g = open("postests.html", "w")
h = open("negtests.html", "w")

fmain = f"""<html
<head><title>TestAnything</title>
</head>
<body style="background-image:url('ipca.png');background-repeat: no-repeat">
<div class="topnav">
    <a href="main.html"><img src="index.png" alt="index"></a>
    <a href="main.html"><img src="home.png" alt="index"></a>
    <a href="postests.html"><img src="post.png" alt="post"></a>
    <a href="negtests.html"><img src="negt.png" alt="negt"></a>
</div>
<p style="text-align:center;font-size:170%"><b><mark style="background:rgb(0, 0, 0);background: rgba(0, 0, 0, 0.5);color:white">TestAnything Result</mark></b></p>
<center>
<table border=15 bgcolor="white">
    <tr>
        <th style="font-size:140%">Tests</th>
        <th style="font-size:140%">Number of tests</th>
    </tr>
    <tr>
        <td style="color:32CD32;font-size:140%;text-align: center">Positive test</td>
        <td style="color:32CD32;font-size:140%;text-align: center">{poscount}</td>
    </tr>
    <tr>
        <td style="color:32CD32;font-size:140%;text-align: center">Positive subtest</td>
        <td style="color:32CD32;font-size:140%;text-align: center">{subposcount}</td>
    </tr>
    <tr>
        <td style="color:#CC0000;font-size:140%;text-align: center">Negative test</td>
        <td style="color:#CC0000;font-size:140%;text-align: center">{negcount}</td>
    </tr>
    <tr>
        <td style="color:#CC0000;font-size:140%;text-align: center">Negative subtest</td>
        <td style="color:#CC0000;font-size:140%;text-align: center">{subnegcount}</td>
    </tr>
    <tr>
        <td style="font-size:140%;text-align: center">Total tests</td>
        <td style="font-size:140%;text-align: center">{totaltests}</td>
    </tr>
    <tr>
        <td style="font-size:140%;text-align: center">Total subtests</td>
        <td style="font-size:140%;text-align: center">{totalsubtests}</td>
    </tr>
</table></center>
</html>"""


gmain = f"""<html
<head><title>TestAnything</title>
</head>
<body style="background-image:url('ipca.png');background-repeat: no-repeat">
<div class="topnav">
    <a href="main.html"><img src="index.png" alt="index"></a>
    <a href="main.html"><img src="home.png" alt="index"></a>
    <a href="postests.html"><img src="post.png" alt="post"></a>
    <a href="negtests.html"><img src="negt.png" alt="negt"></a>
</div>
<p style="text-align:center;font-size:170%;"><b><mark style="background:rgb(0, 0, 0);background: rgba(0, 0, 0, 0.5);color:white">TestAnything Result</mark></b></p>

<p><mark style="background: rgb(0, 0, 0);background: rgba(0, 0, 0, 0.5);color:white;font-size:300%">Positive tests nº :</mark><br> </p>
<p><mark style="background: rgb(0, 0, 0);background: rgba(0, 0, 0, 0.5);color:white;font-size:200%">{postests}</mark></p>
</html>"""


hmain = f"""<html
<head><title>TestAnything</title>
</head>
<body style="background-image:url('ipca.png');background-repeat: no-repeat">
<div class="topnav">
    <a href="main.html"><img src="index.png" alt="index"></a>
    <a href="main.html"><img src="home.png" alt="home"></a>
    <a href="postests.html"><img src="post.png" alt="post"></a>
    <a href="negtests.html"><img src="negt.png" alt="negt"></a>
</div>
<p style="text-align:center;font-size:170%;"><b><mark style="background:rgb(0, 0, 0);background: rgba(0, 0, 0, 0.5);color:white">TestAnything Result</mark></b></p>

<p><mark style="background: rgb(0, 0, 0);background: rgba(0, 0, 0, 0.5);color:white;font-size:300%">Negative tests nº :</mark><br> </p>
<p><mark style="background: rgb(0, 0, 0);background: rgba(0, 0, 0, 0.5);color:white;font-size:200%">{negtests}</mark></p>
</html>"""

f.write(fmain)
f.close()

g.write(gmain)
g.close()

h.write(hmain)
h.close()
webbrowser.open_new_tab("main.html")
