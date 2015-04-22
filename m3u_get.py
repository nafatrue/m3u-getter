#!/usr/bin/python
#author: zevolo
#2015-2015

import os

index = 0
error_msg = []

def check_path(path):
    if (not os.path.exists(path)):
        os.mkdir(path)
    if (not os.path.exists(path) or (not os.path.isdir(path))):
        print "path " + path  + " is not directory"
        return False
    return True

def download_file(url, path):
    global index
    if (not url.startswith("http:")):
        print "not support protocol " + url
        return False
    saved_name = path + "/f" + str(index) + ".ts" #just named as fxxx.ts
    index += 1
    #print saved_name
    wget_file(url, saved_name)
    return True

def wget_file(url, target):
    #if there is an error, retry 5 times!!!
    global error_msg
    for i in range(0, 5):
        if (os.system('wget "'+ url + '" -O ' + target) == 0):
            return True
    info = "failed to download " + url + " to " + target
    print info
    error_msg.append(info)
    return False

def process_file(filename, path):
    if (not check_path(path)):
        return

    f = open(filename)
    newf = open(path+"/1.m3u8", 'w')
    
    lines = f.readlines()
    f.close()
    for l in lines:
        if (l.startswith("http:")):
            #print "file is " + l[:-1]
            download_file(l[:-1], path)
    i = 0
    for l in lines:
        if (l.startswith("http:")):
            s = './f' + str(i) + ".ts\n"
            i += 1
            newf.write(s)
        else:
            newf.write(l)
    newf.close()

    if len(error_msg) != 0:
        print "error:"
        print error_msg
    else:
        print "success to download files"

if __name__ == "__main__":
    process_file("1.m3u", "m3u")

