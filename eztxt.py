#Please excuse the utter terribleness of this, I created this when I was just getting started with python

import os

def delete(name):
    os.remove(name)

def write(name, data):
    str(data)
    f = open(name, "w+")
    f.write(data)
    f.close()

def read(name):
    f = open(name, "r+")
    data = f.read()
    f.close()
    return data

def append(name, data):
    str(data)
    f = open(name, "a+")
    f.write(data)
    f.close()

def appends(name, data):
    str(data)
    dataw = " "+ data
    f = open(name, "a+")
    f.write(dataw)
    f.close()

def appendn(name, data):
    str(data)
    dataw = "\n" + data
    f = open(name, "a+")
    f.write(dataw)
    f.close()

def readline(name, line):
    f = open(name, "r+")
    data = f.readline(int(line))
    f.close()
    return data

def readlines(name):
    f = open(name, "r+")
    data = f.readlines()
    f.close()
    return data