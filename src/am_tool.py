import os
import re 
import status

def sh_exec(cmd):    
    os.system(cmd)


def readDumpFile():
    sh_exec("adb shell dumpsys activity activities -r > " + status.DA)
    f = open(status.DA)
    lines = f.readlines()
    return lines


def getCurrentTaskRecord():
    lines = readDumpFile()
    it = iter(lines)
    line = it.__next__()

    package = None
    activity = None
    while line != None:    
        try:
            line = str.strip(it.__next__())
        except StopIteration:
            break

        if line.startswith("* TaskRecord"):            
            while package is None or activity is None:
                if line.startswith("affinity="):
                    package = str.split(line, "affinity=")[-1]
                elif line.startswith("Activities="):                    
                    activityRecords = str.split(line, "Activities=")[-1]
                    tags = str.split(activityRecords, " ")                    
                    tags.reverse()   
                              
                    for tag in tags:
                        if 'Activity' in tag:
                            activity = tag
                            break
                line = str.strip(it.__next__())    
            break   
    activity = str.split(activity, "/")[-1]            
    return package, activity


def getBackStack(package):
    lines = readDumpFile()
    find = -1
    taskRecord = []
    it = iter(lines)
    line = it.__next__()

    while line != None:
        try:
            line = str.strip(it.__next__())
        except StopIteration:
            break
        
        if line.startswith(package):
            find = 0
        elif find != -1:                                   
            if line.startswith("Run "):
                while(line.startswith("Run")):
                    #print(line)
                    #Run #0: ActivityRecord{3701aa4 u0 com.example.ws3.testapp/.MainActivity t1304}
                    sp = str.split(line, "/")                    
                    p = str.split(sp[0], " ")[-1]
                    a = str.split(sp[1], " ")[0]
                    pa = p + a                    
                    taskRecord.append(pa)                    
                    try:
                        line = str.strip(it.__next__())
                    except StopIteration:
                        break
                break      
            
    return taskRecord


if __name__ == "__main__":
    readDumpFile()
    print("getCurrentTaskRecord:", getCurrentTaskRecord())
    print("getBackStack:", getBackStack(package='affinity=com.taobao.trip'))