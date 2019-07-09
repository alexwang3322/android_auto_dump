import os
import re 
import am_tool 
import status

def sh_exec(cmd):
    os.system(cmd)


def pout(msg):
    print(msg)    


def dumpLayoutXml(path, xml):
    if os.path.exists(xml):
        os.remove(xml)
    if not os.path.exists(path):
        os.makedirs(path)
            
    sh_exec(status.SHELL + " dump " + xml)        


def isDialogWindow(activityName):
    #return False    
    sh_exec(status.SHELL + " windows")
    f = open(status.WN, 'r')
    fline = f.readline()
    fline = str.lstrip(str.rstrip(fline))
    
    t1 = str.split(fline, "=")[-1]
    windows2 = str.split(t1, ",")
    
    if len(windows2) >= 2:
        a = str.split(windows2[0], "}")[-2]
        b = str.split(windows2[1], "}")[-2]
        return a[-10:-1] == b[-10:-1]
    else:
        return False

    

'''
Trun a.b.c into a/b/c/
'''
def getPath(classPath, root=status.DUMP):
    path = str.replace(classPath, ".", "/")
    return root + path + "/"


def activity():
    package, activity = am_tool.getCurrentTaskRecord()    
    return package, activity


def backPress():
    return sh_exec(status.SHELL + " click " + str(x) + " " + str(y))


def click(x, y, resource_id=None):
    sh_exec(status.SHELL + " click " + str(x) + " " + str(y))
    

def text(msg):
    return sh_exec('adb shell input text "' + msg + '"')


def matchBound(bound, pattern="\[-?(\d+),-?(\d+)\]\[-?(\d+),-?(\d+)\]"):
    m = re.match(pattern, bound) 
    l, t, r, b = int(m.groups()[0]), int(m.groups()[1]), int(m.groups()[2]), int(m.groups()[3])
    return (l, t, r, b)


def takeSnapshot(path):
    sh_exec(status.SHELL + " snapshot " + path)    


if __name__ == "__main__":
    #p, a = activity()
    dumpLayoutXml(status.DUMP, status.TXML)
    #print(isDialogWindow(None))
    