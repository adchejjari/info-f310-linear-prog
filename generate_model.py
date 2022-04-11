#from msilib.schema import Binary
import sys




def parseFile(path):
    f = open(path, "r")
    parameters = f.readline().rstrip().split(" ")
    obj, types, conflicts = parameters[0], parameters[1], parameters[2]
    q = f.readline().rstrip()
    parmatersTable = []
    for i in range(int(types)):
        parmatersTable.append([int(element)for element in f.readline().rstrip().split(" ")])
    M  = max(tuple(zip(*parmatersTable))[1])
    print(M)
    conflictsTable = []
    for i in range(int(conflicts)):
        conflictsTable.append([int(element)for element in f.readline().rstrip().split(" ")])
    
    res = open(path + ".lp", "w")
    
    #obj function
    res.write("Minimize \n")
    obj_function = "z_0"
    for c in range(1,int(obj)):
        obj_function += (" + z_"+str(c))
    res.write("     " + obj_function + "\n")
    
    #contraintes
    res.write("Subject To \n")
    constraintList = []
    
    for c in range(int(obj)):
        ctr_1 = ""
        for t in range(int(types)):
            ctr_1 += "{2}x_{0}_{1} + ".format(str(c), str(t), parmatersTable[t][0])
        ctr_1 = ctr_1[:len(ctr_1)-3] + " - " + q + " z_{0}".format(c) + " <= 0" 
        constraintList.append(ctr_1)

    for t in range(int(types)):
        ctr_2 = ""
        for c in range(int(obj)):
            ctr_2 += "x_{0}_{1} + ".format(str(c), str(t))
        ctr_2 = ctr_2[:len(ctr_2)-3] +  " = " + str(parmatersTable[t][1]) 
        constraintList.append(ctr_2)
        
    for t in range(int(types)):
        for c in range(int(obj)):
            ctr_3 = "y_{0}_{1} - x_{0}_{1} <= 0".format(str(c), str(t))
            constraintList.append(ctr_3)
        
    for t in range(int(types)):
        for c in range(int(obj)):
            ctr_4 = "x_{0}_{1} - {2}y_{0}_{1} <= 0".format(str(c), str(t), str(M))
            constraintList.append(ctr_4)
          
    if(int(args[2]) > 0):
        #special contrainte 1
        for t in range(int(types)):
            ctr_5 = ""
            for c in range(int(obj)):
                ctr_5 += "y_{0}_{1} + ".format(str(c), str(t))
            ctr_5 = ctr_5[:len(ctr_5)-3] +  " <= " + str(parmatersTable[t][2]) 
            constraintList.append(ctr_5)
                  
    index = 0
    for ctr in constraintList:
        res.write("    ctr_{0}: ".format(index) + ctr + "\n")
        index += 1
    
    #variables
    res.write("Binary \n")
    for c in range(int(obj)):
        res.write("     z_{0}".format(c) + "\n")
    for c in range(int(obj)):
        for t in range(int(types)):
            res.write("     y_{0}_{1}".format(c, t) + "\n")
    res.write("Integer \n")
    for c in range(int(obj)):
        for t in range(int(types)):
            res.write("     x_{0}_{1}".format(c, t) + "\n")   
    res.write("End")
    
    
        


if __name__ == '__main__':
    args = sys.argv
    instance = args[1]
    p = int(args[2])
    parseFile(instance)



