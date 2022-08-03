from functionengine import functionvalue,trigonemetricfunctionvalue
import math

def listtostring(listx):
    q=""
    i=0
    while i<len(listx)-1:
        q +=listx[i]
        i+=1
    q +=listx[i]
    return q

def getvalue_function_old(stringlist,valuex):
    st=list()
    i=0
    y1=0
    funclist=list()
    alphe=["s","i","n","c","o","t","a","e","p"]
    while i<len(strlist)-1:
        if (strlist[i]=="x") or (strlist[i]=="("):
            i +=1
            while not(strlist[i]==")"):
                    funclist.append(strlist[i])
                    i +=1
            
            if ss=="+":
                    y1 +=functionvalue(listtostring(funclist),valuex)
            elif ss=="-":
                    y1 +=(functionvalue(listtostring(funclist),valuex)*-1)
            elif ss=="/":
                    y1= y1/functionvalue(listtostring(funclist),valuex)
            elif ss=="*":
                    y1 =y1*functionvalue(listtostring(funclist),valuex)
            funclist=list()
        
        
            
        
            
        if (strlist[i] in alphe):
            while not(strlist[i]=="^" or strlist[i]=="("):
                triglist.append(strlist[i])
                i +=1
            if (strlist[i]=="("):
                i+=1
                while not(strlist[i]==")"):
                    funclist.append(strlist[i])
                    i +=1
                
                trigvalue=functionvalue(listtostring(funclist),valuex)
                yy=float(trigonemetricfunctionvalue(triglist,trigvalue))
                
                #print(ss)
                if ss=="+":
                    y1 =y1+yy
                if ss=="-":
                    y1 += (yy*-1)
                if ss=="/":
                    y1= y1/(yy)
                if ss=="*":
                    y1 =y1*yy
                funclist=list()
                triglist=list()
                #i +=1
                
                
               
                
            elif (strlist[i]=="^"):
                n=strlist[i+1]
                
                i +=3
                while not(strlist[i]==")"):
                    funclist.append(strlist[i])
                    i +=1
                
                trigvalue=functionvalue(listtostring(funclist),valuex)
                funclist=list()
                i +=1
                trig=trigonemetricfunctionvalue(triglist,trigvalue)
                if ss=="+":
                    y1 +=pow(trig,float(n))
                elif ss=="-":
                    y1 +=(pow(trig,float(n))*-1)
                elif ss=="/":
                    y1= y1/(pow(trig,float(n)))
                elif ss=="*":
                    y1 =y1*pow(trig,float(n))

        elif strlist[i]=="+" or "-" or "/" or "*":
            ss=strlist[i]
            

       
       
        
        

        i +=1
        
        
            
            

    return y1

def get_function_only(function):
    function = list(function)
    # identify symbols and function
    trigfunc = ["sin", "cos", "tan", "exp", "log"]
    hypertrigfunc = ["sinh", "cosh", "tanh"]
    symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "+", "-", "*", "/", "(", ")"]
    # create th enew function variable to set the new function
    new_function = ""
    i = 0
    while i < len(function):
        if function[i] == "^":
            new_function += "**"
        elif function[i] == "x":
            new_function += "x"
        elif (i+3 < len(function)):
            if (f"{function[i]}{function[i+1]}{function[i+2]}" in trigfunc) and function[i+3] == "(":
                new_function += f"math.{function[i]}{function[i+1]}{function[i+2]}"
                i += 2
        elif (i+4 < len(function)):
            if (f"{function[i]}{function[i+1]}{function[i+2]}{function[i+3]}" in hypertrigfunc) and function[i+4] == "(":
                new_function += f"math.{function[i]}{function[i+1]}{function[i+2]}{function[i+3]}"
                i += 3
        if function[i] in symbols:
            new_function += function[i]
        i += 1
    return new_function

def getvalue_function(function, valuex):
    new_function = ""
    for i in range(0, len(function)):
        if function[i] == "x":
            if i+1 < len(function) and i-1 >= 0 and (function[i-1] == "e" and function[i+1] == "p"):
                new_function += function[i]
            else:
                new_function += f"({str(valuex)})"
        else:
            new_function += function[i]

    return eval(new_function)

        
        
