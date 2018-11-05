import string
from enum import Enum
from search import *
from PIL import Image,ImageFont,ImageDraw,ImageEnhance,ImageColor
import datetime


class Direction(Enum):
    RIGHT=0
    LEFT=1
    DOWN=2
    TOP=3

class PegProblem(Problem):
    def __init__(self):
        self.initial = "D3"
        self.pathCost = 0
        self.m_invalidHoles = ["A0","B0","F0","G0","A1","B1","F1","G1","A5","B5","F5","G5","A6","B6","F6","G6"]
        
    def actions(self, state):
        playablePegs = self.GetPlayablePegs(state)
        return playablePegs
        
    def result(self, state, action):
        playablePegs = self.GetPlayablePegs(state)
        allEmptyHolesAfterPegMoving = self.GetEmptyHolesAfterPlayingPeg(state,playablePegs)
        newNodesForTree = self.GetNextEmptyHolesWithComma(allEmptyHolesAfterPegMoving)
        for i,nodes in enumerate(newNodesForTree):
            if action in nodes:
                return newNodesForTree[i]

    def goal_test(self, state):
        #print("Playable Peg Count: and State",len(self.GetPlayablePegs(state)),state)
        if len(self.GetPlayablePegs(state))>0:
            return False
        else:
            print("Final State: ",state)
            self.finalState = state
            print("Path Cost: ",self.pathCost)
            return True

        
    def path_cost(self, c, state1, action, state2):
        self.pathCost += 1
    def value(self, state):
        pass
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
    
    def drawResultImage(self):
        resultImage = Image.new("RGB",(200,200),color=ImageColor.getrgb('purple'))
        draw = ImageDraw.Draw(resultImage)
        font = ImageFont.truetype("arial.ttf", 22)
        cell_width = 25
        cell_height = 25
        
        for val in range(7):
            draw.text((0,(val*cell_height)+cell_width),str(val),fill="yellow",font=font)
            draw.text(((val*cell_width+cell_width),0),str(chr(ord('A')+val)),fill="yellow",font=font)

        #draw invalid holes with color black

        for peg_chr in range(7):
            for peg_num in range(7):
                number = peg_num
                cell_offset_x = 25
                cell_offset_y = 25
                character_number = peg_chr
                draw.rectangle(((cell_offset_x+((character_number)*cell_width),cell_offset_y+(number*cell_height)),(cell_height+cell_offset_x+((character_number)*cell_width),cell_width+cell_offset_y+(number*cell_height))),fill="orange",outline="gray")
        
        for val in self.m_invalidHoles:
            character = val[0]
            number = int(val[1])
            cell_offset_x = 25
            cell_offset_y = 25

            character_number = ord(character)-ord('A')
            draw.rectangle(((cell_offset_x+((character_number)*cell_width),cell_offset_y+(number*cell_height)),(cell_height+cell_offset_x+((character_number)*cell_width),cell_width+cell_offset_y+(number*cell_height))),fill="black")
        
        for val in self.finalState.split(','):
            character = val[0]
            number = int(val[1])
            cell_offset_x = 25
            cell_offset_y = 25

            character_number = ord(character)-ord('A')
            draw.rectangle(((cell_offset_x+((character_number)*cell_width),cell_offset_y+(number*cell_height)),(cell_height+cell_offset_x+((character_number)*cell_width),cell_width+cell_offset_y+(number*cell_height))),fill="purple",outline='gray')

        out_time = datetime.datetime.now().time()    
        resultImage.save("result_"+str(out_time.hour)+"_"+str(out_time.minute)+"_"+str(out_time.second)+".png")
        print("Output of final state image is completed.\n\t(*)Color orange shows pegs.\n\t(*)Color black shows invalid areas of game board.\nYou can view the image at current directory")


if __name__=="__main__":
    pp = PegProblem()
    if len(sys.argv) != 2:
        print("You can execute this file with following prototype\n ./exe_name <bfs or dfs or astar>\nExample: py ./main.py bfs")
    else:
        if str(sys.argv[1]).lower() == "bfs":
            breadth_first_tree_search(pp)
            pp.drawResultImage()
        elif str(sys.argv[1]).lower() == "dfs":
            depth_first_tree_search(pp)
            pp.drawResultImage()
        elif str(sys.argv[1]).lower() == "astar":
            astar_search(pp)
            pp.drawResultImage()
        else:
            print("You typed invalid arguments. Arguments should be bfs, dfs or astar")    


    