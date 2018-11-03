from treelib import *
import string
from enum import Enum

class Direction(Enum):
    RIGHT=0
    LEFT=1
    DOWN=2
    TOP=3

class PegApplication():

    def __init__(self):
        self.tree = Tree()
        self.tree.create_node("D3","D3",data=0)  # root node
        
        self.m_invalidHoles = ["A0","B0","F0","G0","A1","B1","F1","G1","A5","B5","F5","G5","A6","B6","F6","G6"]
        playablePegs = self.GetPlayablePegs("D3")

        print("Valid Playable Peg: ",*playablePegs)
                 
        
    def GetEmptyHolesAfterPlayingPeg(self,currentEmptyHole,validHole):
        if currentEmptyHole[0] == validHole[0]: #Harfler aynı ise
            if (int(currentEmptyHole[1]) > int(validHole[1])):
                return [validHole,validHole[0]+str(int(validHole[1])+1)] 
            else:
                return [validHole,validHole[0]+str(int(validHole[1])-1)]
        else: #Sayılar aynı ise
            if (ord(currentEmptyHole[0]) > ord(validHole[0])):
                return [validHole,chr(ord(validHole[0])+1)+currentEmptyHole[1]]
            else:           
                return [validHole,chr(ord(currentEmptyHole[0])+1)+currentEmptyHole[1]]

    def IsNextHoleEmpty(self,holes,hole,direction):
        test_hole = ""
        if Direction.RIGHT == direction:
            test_hole = chr(ord(hole[0])+1)+hole[1]  
        elif Direction.LEFT == direction:
            test_hole = chr(ord(hole[0])-1)+hole[1]
        elif Direction.DOWN == direction:
            test_hole = hole[0]+str(int(hole[1])+1)
        elif Direction.TOP == direction:
            test_hole = hole[0]+str(int(hole[1])-1)

        print("Test Next Hole and Direction: ",test_hole,direction)
        if test_hole in holes:
            return True
        else:
            return False 

    def CheckPegValid(self,case):
        print("Check Peg Valid Test:",case)
        if len(case)>3:
            return False

        least_str_ord = ord('A')
        most_str_ord = ord('G')
        case_str_ord = ord(case[0])
        case_num_ord = -1
        try:
            case_num_ord = int(case[1])
        except:
            case_num_ord = -1    

         
        if (case_str_ord < least_str_ord) or (case_str_ord > most_str_ord): 
            return False
        elif (case_num_ord > 6) or (case_num_ord<0):
            return False
        elif case in self.m_invalidHoles:
            return False
        else:
            return True        


    def GetPlayablePegs(self,holes):
        validCaseslist = []
        
        print("Holes:", holes)
        for hole in holes.split(','):
            case1 = chr(ord(hole[0]) + 2) + hole[1] #right
            case2 = chr(ord(hole[0]) - 2) + hole[1] #left
            case3 = chr(ord(hole[0])) + str(int(hole[1])+2) #down
            case4 = chr(ord(hole[0])) + str(int(hole[1])-2) #top

            if self.CheckPegValid(case1) and not self.IsNextHoleEmpty(holes,hole,Direction.RIGHT) :
                validCaseslist.append(case1)
            if self.CheckPegValid(case2) and not self.IsNextHoleEmpty(holes,hole,Direction.LEFT) :
                validCaseslist.append(case2)
            if self.CheckPegValid(case3) and not self.IsNextHoleEmpty(holes,hole,Direction.DOWN) :
                validCaseslist.append(case3)
            if self.CheckPegValid(case4) and not self.IsNextHoleEmpty(holes,hole,Direction.TOP) :
                validCaseslist.append(case4)

        return validCaseslist








        
        


        
        
    


if __name__=="__main__":
    serverPort=12000
    PegApplication()
    
