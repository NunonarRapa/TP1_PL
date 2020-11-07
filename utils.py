# utils.py
# As nossas funções uteis

def readFile(filename):
    fh = open(filename, mode="r")
    contents = fh.read()
    fh.close()
    return contents

