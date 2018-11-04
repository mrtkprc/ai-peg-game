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
        self.tree.create_node("D3",data=0)  # root node

        self.root_id = self.tree.root
                
        self.m_invalidHoles = ["A0","B0","F0","G0","A1","B1","F1","G1","A5","B5","F5","G5","A6","B6","F6","G6"]
        #rootHole = "E5,D6,E6,E3,E2,E1,B2,B3,B4,C2,C1,C0,D2,D1,D0,C6,D3,F2,C4,F4,D5,C3,F3"
        rootHole = "D3"
        #playablePegs = self.GetPlayablePegs(rootHole)
        #print("Playable Pegs", playablePegs)
        #allEmptyHolesAfterPegMoving = self.GetEmptyHolesAfterPlayingPeg(rootHole,playablePegs)
        #newNodesForTree = self.GetNextEmptyHolesWithComma(allEmptyHolesAfterPegMoving)
        #print(newNodesForTree)

        #self.CreateTreeWithRecursion(rootHole,self.root_id)
        self.CreateTreeWithLoop(rootHole,self.root_id)
        self.tree.show()

    def CreateTreeWithLoop(self,emptyHole,parID):

        self.tree.show()

        emptyHoleData = emptyHole
        parentID = parID

        playablePegs = self.GetPlayablePegs(emptyHoleData)

        if len(playablePegs) == 0:
            return

        allEmptyHolesAfterPegMoving = self.GetEmptyHolesAfterPlayingPeg(emptyHoleData,playablePegs)
        newNodesForTree = self.GetNextEmptyHolesWithComma(allEmptyHolesAfterPegMoving)
        lastparentID =  ""
        for node in newNodesForTree:
            lastparentID = self.tree.create_node(node,parent=parentID)    

        all_leaves_empty_holes = []    
        all_leaves_empty_holes.append(lastparentID)
        for sibling in self.tree.siblings(lastparentID.identifier):
            all_leaves_empty_holes.append(sibling)

        
        for leaf in all_leaves_empty_holes:
            self.CreateTreeWithLoop(leaf.tag,leaf.identifier)
            

        
        
    def CreateTreeWithRecursion(self,emptyHoleData,parentID):
        
        playablePegs = self.GetPlayablePegs(emptyHoleData)
        allEmptyHolesAfterPegMoving = self.GetEmptyHolesAfterPlayingPeg(emptyHoleData,playablePegs)
        newNodesForTree = self.GetNextEmptyHolesWithComma(allEmptyHolesAfterPegMoving)

        if len(newNodesForTree) == 0:
            return

        for i,node in enumerate(newNodesForTree):
            created_node = self.tree.create_node(node,parent = parentID)
            self.CreateTreeWithRecursion(node,created_node.identifier)
            

           
        

    def GetNextEmptyHolesWithComma(self,allPossibles):
        all_pos_strings = []
        for possible in allPossibles:
            possible_str = ""
            for pos in possible:
                possible_str += pos+","
            possible_str = possible_str[:-1]    
            all_pos_strings.append(possible_str)
        
        return all_pos_strings    


    def GetEmptyHolesAfterPlayingPeg(self,currentEmptyHoles,playablePegs):
        allValidEmptyHoles = []
        for playablePeg in playablePegs:
            peg_move_right = self.GetMovePegPosition(playablePeg,Direction.RIGHT,2)
            peg_move_left = self.GetMovePegPosition(playablePeg,Direction.LEFT,2)
            peg_move_down = self.GetMovePegPosition(playablePeg,Direction.DOWN,2)
            peg_move_top = self.GetMovePegPosition(playablePeg,Direction.TOP,2)

            cur_emp_holes = currentEmptyHoles.split(',')
            
            for i, emp_hol in enumerate(cur_emp_holes):
                #print("Playable Peg and Empty Hole",playablePeg,emp_hol)
                if (peg_move_right == emp_hol and not self.GetMovePegPosition(playablePeg,Direction.RIGHT,1) in cur_emp_holes):
                    cur_emp_holes[i] = playablePeg
                    cur_emp_holes.insert(0,self.GetMovePegPosition(playablePeg,Direction.RIGHT,1))
                    break
                elif (peg_move_left == emp_hol and not self.GetMovePegPosition(playablePeg,Direction.LEFT,1) in cur_emp_holes):
                    cur_emp_holes[i] = playablePeg
                    cur_emp_holes.insert(0,self.GetMovePegPosition(playablePeg,Direction.LEFT,1))
                    break
                elif (peg_move_down == emp_hol and not self.GetMovePegPosition(playablePeg,Direction.DOWN,1) in cur_emp_holes):
                    cur_emp_holes[i] = playablePeg
                    cur_emp_holes.insert(0,self.GetMovePegPosition(playablePeg,Direction.DOWN,1))    
                    break
                elif (peg_move_top == emp_hol and not self.GetMovePegPosition(playablePeg,Direction.TOP,1) in cur_emp_holes):
                    cur_emp_holes[i] = playablePeg
                    cur_emp_holes.insert(0,self.GetMovePegPosition(playablePeg,Direction.TOP,1))
                    break

            allValidEmptyHoles.append(cur_emp_holes)        

        return allValidEmptyHoles            

    def GetMovePegPosition(self,peg,direction,move_count = 1):
        moved_peg = ""
        if Direction.RIGHT == direction:
            moved_peg = chr(ord(peg[0])+move_count)+peg[1]  
        elif Direction.LEFT == direction:
            moved_peg = chr(ord(peg[0])-move_count)+peg[1]
        elif Direction.DOWN == direction:
            moved_peg = peg[0]+str(int(peg[1])+move_count)
        elif Direction.TOP == direction:
            moved_peg = peg[0]+str(int(peg[1])-move_count)    

        return moved_peg    

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

        #print("Test Next Hole and Direction: ",test_hole,direction)
        if test_hole in holes:
            return True
        else:
            return False 

    def CheckPegValid(self,case):
        #print("Check Peg Valid Test:",case)
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
        
        #print("Holes:", holes)
        for hole in holes.split(','):
            #print("Hole: ",hole)
            case1 = chr(ord(hole[0]) + 2) + hole[1] #right
            case2 = chr(ord(hole[0]) - 2) + hole[1] #left
            case3 = chr(ord(hole[0])) + str(int(hole[1])+2) #down
            case4 = chr(ord(hole[0])) + str(int(hole[1])-2) #top

            if holes.find(str(case1)) == -1 and self.CheckPegValid(case1) and not self.IsNextHoleEmpty(holes,hole,Direction.RIGHT) :
                validCaseslist.append(case1)
            if holes.find(str(case2)) == -1 and self.CheckPegValid(case2) and not self.IsNextHoleEmpty(holes,hole,Direction.LEFT) :
                validCaseslist.append(case2)
            if holes.find(str(case3)) == -1 and self.CheckPegValid(case3) and not self.IsNextHoleEmpty(holes,hole,Direction.DOWN) :
                validCaseslist.append(case3)
            if holes.find(str(case4)) == -1 and self.CheckPegValid(case4) and not self.IsNextHoleEmpty(holes,hole,Direction.TOP) :
                validCaseslist.append(case4)

        return validCaseslist

if __name__=="__main__":
    serverPort=12000
    PegApplication()
    
