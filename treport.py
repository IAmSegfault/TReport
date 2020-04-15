import shelve
from settings import *
from datetime import datetime
from os import path as p
from os import makedirs

if __name__ == "__main__":

    if not p.exists(RUNTIME_SETTINGS):
        makedirs(RUNTIME_DIR)



    text = []
    with open(LOG_TEST) as f:

        text = [i for i in f.read().split('\n')]
        text = text[2:]
        f.close()
    line = []
    for i in range(len(text)):
        line = text[i].split(",")
        d = line[0].strip('"')
        t = line[1].strip('"')[:-3]
        stamp = d + "." + t
        dt = datetime.strptime(stamp, "%m/%d/%Y.%I:%M:%S")

        print(dt)

    #print(len(text))
    #print(text[0])