from msilib.schema import Binary
import sys

import constraint



def parseFile(path):
    f = open(path, "r")
    parameters = f.readline().rstrip().split(" ")
    obj, types, conflicts = parameters[0], parameters[1], parameters[2]
    c = f.readline().rstrip()
    parmatersTable = []
    for i in range(int(types)):
        parmatersTable.append([int(element)for element in f.readline().rstrip().split(" ")])
    
    conflictsTable = []
    for i in range(int(conflicts)):
        conflictsTable.append([int(element)for element in f.readline().rstrip().split(" ")])
    
    res = open(path + ".lp", "w")
    res.write("Minimize \n")
    obj_function = "x_0"
    for i in range(1,int(obj)):
        obj_function += (" + x_"+str(i))
    res.write("     " + obj_function + "\n")
    res.write("Subject To \n")
    constraintList = []
    ctr_1 = ""
    for i in range(int(obj)):
        for j in range(int(obj)):
            ctr_1 += "y_{0}_{1} + ".format(int(i), int(j))
    ctr_1 = ctr_1[:len(ctr_1)-3] + " = " + str(obj)
    constraintList.append(ctr_1)
    s = []
    for param in parmatersTable:
        for i in range(param[1]):
            s.append(param[0])
    
    for i in range(int(obj)):
        ctr_2 = ""
        for j in range(int(obj)):
            ctr_2 += "y_{0}_{1} * {2} + ".format(str(i), str(j), s[j])
        ctr_2 = ctr_2[:len(ctr_2)-3] + " <= " + c
        constraintList.append(ctr_2)
        
    index = 0
    for ctr in constraintList:
        res.write("    ctr_{0}: ".format(index) + ctr + "\n")
        index += 1
    
    res.write("Binary \n")
    for i in range(int(obj)):
        res.write("     x_{0}".format(i) + "\n")
    for i in range(int(obj)):
        for j in range(int(obj)):
            res.write("     y_{0}_{1}".format(i, j) + "\n")
    res.write("End")
    
    
        
















if __name__ == '__main__':
    args = sys.argv
    instance = args[1]
    p = int(args[2])
    parseFile(instance)



