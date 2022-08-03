import math

def functionengine(functionstring):
    i=0
    s=1
    q=""
    listint=["0","1","2","3","4","5","6","7","8","9","."]
    funclist=list(functionstring)
    dictfunc=[]
    n=""
    powern=1
    if funclist[0]=="x" or funclist[0]=="X":
        i+=2
        while not(funclist[i]=="+" or funclist[i]=="-"):
            if funclist[i]=="n":
                powern=-1
            else:
                n +=funclist[i]
            i+=1
        dictfunc.append((1,powern*float(n)))
        n=""
        powern=1

    while i<len(funclist):
        if (funclist[i]=="x" or funclist[i]=="X") and (funclist[i+1]=="+" or funclist[i+1]=="-"):
            dictfunc.append((float(q)*s,1))
            q=""
            s=1
        elif funclist[i] in listint:
            q +=funclist[i]
        elif (funclist[i]=="x" or funclist[i]=="X") and (funclist[i+1]=="^"):
            i+=2
            while not(funclist[i]=="+" or funclist[i]=="-"):
                      if funclist[i]=="n":
                          powern=-1
                      else:
                          n+=funclist[i]
                      i+=1
            if q=="":
                q="1"
            q=float(q)*s
            dictfunc.append((float(q),powern*float(n)))
            powern=1
            q=""
            s=1
            i +=(-1)
            n=""
        elif funclist[i]=="+":
            s=s*1
        elif funclist[i]=="-":
            s=s*(-1)
        
            
            
        i +=1
    dictfunc.append((float(q)*s,0))
    return dictfunc

def valueoffunction(dictfunc,valuex):
    value=0
    for m in range(0,len(dictfunc)):
        value += (dictfunc[m][0]*pow(valuex,dictfunc[m][1]))

    return value

def functionvalue(functionstring,valuex):
    return valueoffunction(functionengine(functionstring),valuex)

def trigonemetricfunctionvalue(trigstring,valuex):
    if trigstring==["s","i","n"]:
        return math.sin(valuex)
    elif trigstring==["c","o","s"]:
        return math.cos(valuex)
    elif trigstring==["t","a","n"]:
        return math.tan(valuex)
    elif trigstring==["s","e","c"]:
        return (pow(math.cos(valuex),-1))
    elif trigstring==["c","o","s","e","c"]:
        if math.sin(valuex)==0.0:
            return 100000000
        elif not(math.sin(valuex)==0.0):
            return (pow(math.sin(valuex),-1))
    elif trigstring==["c","o","t"]:
        return (pow(math.tan(valuex),-1))
    elif trigstring==["e","x","p"]:
        return math.exp(valuex)
    elif trigstring==["s","i","n","h"]:
        return math.sinh(valuex)
    elif trigstring==["c","o","s","h"]:
        return math.cosh(valuex)
    elif trigstring==["t","a","n","h"]:
        return math.tanh(valuex)
    
    

