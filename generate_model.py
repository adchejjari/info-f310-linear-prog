import sys

class ModelGenerator:
    
    def __init__(self, filePath, p):
        
        self.filePath = filePath
        self.p = int(p)
        self.parseParameters()
        
    def parseParameters(self):
        
        f = open(self.filePath, "r")
        parameters = f.readline().rstrip().split(" ")
        # n = nombre d'objets, T = nombre de types, I = nombre d'incompatibilites
        self.id = self.filePath[:len(self.filePath)-4].split("_")[-1]
        self.n, self.T, self.I = int(parameters[0]), int(parameters[1]), int(parameters[2])
        self.q = f.readline().rstrip()  #capacité de la boite
        self.parmatersTable = []
        for t in range(self.T):
            # [taille du type t, nbr d'objets du type t, b_t]
            self.parmatersTable.append([int(element)for element in f.readline().rstrip().split(" ")])
        self.M  = max(tuple(zip(*self.parmatersTable))[1])  #big M 
        self.conflictsTable = []
        for i in range(self.I):
            self.conflictsTable.append([int(element)for element in f.readline().rstrip().split(" ")])
        
    def generateModel(self):
        
        model = open("model_{0}_{1}_{2}_{3}_{4}.lp".format(self.n, self.T, self.I, self.id, self.p), "w")
    
        #fonction objet
        model.write("Minimize \n")
        obj_function = "z_0"
        
        for c in range(1,self.n):
            obj_function += (" + z_"+str(c))
        model.write("     " + obj_function + "\n")
        
        #contraintes
        model.write("Subject To \n")
        constraintList = []
        
        for c in range(self.n):
            # poids total des objets dans une boite <= q
            ctr_1 = ""
            for t in range(self.T):
                ctr_1 += "{2}x_{0}_{1} + ".format(str(c), str(t), self.parmatersTable[t][0])
            ctr_1 = ctr_1[:len(ctr_1)-3] + " - " + self.q + " z_{0}".format(c) + " <= 0" 
            constraintList.append(ctr_1)

        for t in range(self.T):
            # nombre total d'objets de type t stocké = n_t
            ctr_2 = ""
            for c in range(self.n):
                ctr_2 += "x_{0}_{1} + ".format(str(c), str(t))
            ctr_2 = ctr_2[:len(ctr_2)-3] +  " = " + str(self.parmatersTable[t][1]) 
            constraintList.append(ctr_2)
            
        for t in range(self.T):
            # si X_c_t = 0 alors Y_c_t = 0
            for c in range(self.n):
                ctr_3 = "y_{0}_{1} - x_{0}_{1} <= 0".format(str(c), str(t))
                constraintList.append(ctr_3)
            
        for t in range(self.T):
            # si X_c_t > 0 alors Y_c_t = 1
            for c in range(self.n):
                ctr_4 = "x_{0}_{1} - {2}y_{0}_{1} <= 0".format(str(c), str(t), str(self.M))
                constraintList.append(ctr_4)
        
        if(self.p == 1 or self.p == 2):
            #premiere contrainte additionelle 
            for t in range(self.T):
                ctr_5 = ""
                for c in range(self.n):
                    ctr_5 += "y_{0}_{1} + ".format(str(c), str(t))
                ctr_5 = ctr_5[:len(ctr_5)-3] +  " <= " + str(self.parmatersTable[t][2]) 
                constraintList.append(ctr_5)

        if (self.p == 2):
            #deuxieme contrainte additionelle
            for c in range(self.n):
                for conflict in self.conflictsTable:
                    ctr_6 = ""
                    for t in conflict:
                        ctr_6 += "y_{0}_{1} + " .format(str(t), c)
                    ctr_6 = ctr_6[:len(ctr_6)-3] + " <= 1"
                    constraintList.append(ctr_6)

        index = 0
        for ctr in constraintList:
            model.write("    ctr_{0}: ".format(index) + ctr + "\n")
            index += 1
        
        #variables
        model.write("Binary \n")
        for c in range(self.n):
            model.write("     z_{0}".format(c) + "\n")
        for c in range(self.n):
            for t in range(self.T):
                model.write("     y_{0}_{1}".format(c, t) + "\n")
                
        model.write("Integer \n")
        for c in range(self.n):
            for t in range(self.T):
                model.write("     x_{0}_{1}".format(c, t) + "\n")
                   
        model.write("End")        

    
if __name__ == '__main__':
    
    args = sys.argv
    modelGenerator = ModelGenerator(args[1], args[2])
    modelGenerator.generateModel()



