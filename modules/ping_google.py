from os import system

def process():
    result = system("ping www.google.com")
    if (result == 0):
     str = "Google up and running"
    else:
     str = "There might be some problem"
    return str