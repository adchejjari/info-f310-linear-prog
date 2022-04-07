import sys



def parseFile(path):
    f = open(path, "r")
    parameters = f.readline().rstrip().split(" ")
    obj, types, conflicts = parameters[0], parameters[1], parameters[2]
    c = f.readline().rstrip()
    resList=[]
    for i in range(int(types)):
        resList.append([int(element)for element in f.readline().rstrip().split(" ")])
    print(resList)
















if __name__ == '__main__':
    args = sys.argv
    instance = args[1]
    p = int(args[2])
    parseFile(instance)



