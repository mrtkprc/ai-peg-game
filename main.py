from treelib import *
import string


class PegApplication():

    def __init__(self):
        self.tree = Tree()
        self.tree.create_node("D3", "D3")  # root node
        #self.tree.show()
        self.m_invalidHoles = ["A0","B0","F0","G0","A1","B1","F1","G1","A5","B5","F5","G5","A6","B6","F6","G6"]
        
        self.GetValiableMovement(self.tree.root)
        
    def GetEmptyHolesAfterRemovingPeg(self,currentEmptyHole,validHole):
        if currentEmptyHole[0] == validHole[0]:
            if (int(currentEmptyHole[1]) > int(currentEmptyHole[1])):
                return [validHole,validHole[0]+chr(int(validHole)+1)] 
            else:
                return [validHole,validHole[0]+chr(int(validHole)-1)]
        else: #bu elseden itibaren devam et 
            if (int(currentEmptyHole[1]) > int(currentEmptyHole[1])):
                pass
            else:           
                pass

    def CheckCaseValid(self,case):
        print("Case :",case)
        least_str_ord = ord('A')
        most_str_ord = ord('G')
        case_str_ord = ord(case[0])
        case_num_ord = int(case[1])

        if (case_str_ord < least_str_ord) or (case_str_ord > most_str_ord): 
            return False
        elif (case_num_ord > 6) or (case_num_ord<0):
            return False
        elif case in self.m_invalidHoles:
            return False
        else:
            return True

    def GetValiableMovement(self,hole):
        validCaseslist = []

        case1 = chr(ord(hole[0]) + 2) + hole[1]
        case2 = chr(ord(hole[0]) - 2) + hole[1]
        case3 = chr(ord(hole[0])) + str(int(hole[1])+2)
        case4 = chr(ord(hole[0])) + str(int(hole[1])-2)
        
        if self.CheckCaseValid(case1):
            validCaseslist.append(case1)
        if self.CheckCaseValid(case2):
            validCaseslist.append(case2)
        if self.CheckCaseValid(case3):
            validCaseslist.append(case3)    
        if self.CheckCaseValid(case4):
            validCaseslist.append(case4)
        
        return validCaseslist








        
        


        
        
    


if __name__=="__main__":
    serverPort=12000
    PegApplication()
    