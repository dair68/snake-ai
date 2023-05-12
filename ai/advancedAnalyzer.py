#module hosting AdvancedSnakeAnalyzer class
from ai.analyzer import SnakeAnalyzer

#class that incorporates hamiltonian cycles into analysis
class AdvancedSnakeAnalyzer(SnakeAnalyzer):
    #constructor
    #@param game - SnakeGame object that this object will analyze
    def __init__(self, game):
        super().__init__(game)
    
    #finds hamiltonian cycle within rectangular submatrix
    #@param matrix - nested lists forming matrix
    #@param x1 - upper left column number
    #@param y1 - upper left row number
    #@param x2 - lower right column number
    #@param y2 - lower right row number
    #updates rect [x1,y1,x2,y2] of matrix s.t. matrix[i][j]
    #   maps to next space in cycle. inputted rect be even length and/or width
    def rectHCycle(self, matrix, x1, y1, x2, y2):
        m = x2 - x1 + 1
        n = y2 - y1 + 1
        assert self.__evenRect(x1, y1, x2, y2)
        
        #checking if there are even number of columns
        if m % 2 == 0:
            #creating rectangle loops spanning rectangle
            for col in range(x1, x2, 2):
                self.clockwiseRectLoop(matrix, col, y1, col+1, y2)
                
            #merging loops together to form one cycle
            for col in range(x1+1, x2, 2):
                self.__mergeCycles(matrix, col, y1)
        else:
            #creating rectangle loops spanning rectangle
            for row in range(y1, y2, 2):
                self.clockwiseRectLoop(matrix, x1, row, x2, row+1)
                
            #merging loops together to form one cycle
            for row in range(y1+1, y2, 2):
                self.__mergeCycles(matrix, x1, row)
        
    #creates clockwise rectangular loop within rectangular submatrix
    #@param matrix - nested lists forming matrix
    #@param x1 - upper left column number
    #@param y1 - upper left row number
    #@param x2 - lower right column number
    #@param y2 - lower right row number
    #updates rect [x1,y1,x2,y2] of matrix s.t. matrix[i][j]
    #   maps to next space in loop. loop is in a rectangle spanning rect edges
    def clockwiseRectLoop(self, matrix, x1, y1, x2, y2):
        #forming top and bottom edges of loop
        for col in range(x1, x2):
            matrix[col][y1] = (col + 1, y1)
            matrix[col+1][y2] = (col, y2)
            
        #forming left and right edges of loop
        for row in range(y1, y2):
            matrix[x2][row] = (x2, row + 1)
            matrix[x1][row+1] = (x1, row)
            
    #creates counterclockwise rectangular loop within rectangular submatrix
    #@param matrix - nested lists forming matrix
    #@param x1 - upper left column number
    #@param y1 - upper left row number
    #@param x2 - lower right column number
    #@param y2 - lower right row number
    #updates rect [x1,y1,x2,y2] of matrix s.t. matrix[i][j]
    #   maps to next space in loop. loop is in a rectangle spanning rect edges
    def counterClockwiseRectLoop(self, matrix, x1, y1, x2, y2):
        #forming top and bottom edges of loop
        for col in range(x1, x2):
            matrix[col][y2] = (col + 1, y2)
            matrix[col+1][y1] = (col, y1)
            
        #forming left and right edges of loop
        for row in range(y1, y2):
            matrix[x1][row] = (x1, row + 1)
            matrix[x2][row+1] = (x2, row)
            
    #attempts to merge two hamiltonian cycles together
    #@param matrix - nested lists forming movement matrix
    #@param x - upper left column number
    #@param y - upper left row number
    #updates matrix to have mapping now include two cyles merged into one,
    #   merge occurs within square (x, y, x+1, y+1)
    #   returns True if merge occured, False otherwise
    def __mergeCycles(self, matrix, x, y):
        assert x < len(matrix) - 1
        assert y < len(matrix) - 1
        
        #checking if edges are parallel
        if matrix[x][y] == (x+1,y) and matrix[x+1][y+1] == (x,y+1):
            #print("horizontal merge")
            matrix[x][y] = (x, y+1)
            matrix[x+1][y+1] = (x+1, y)
            return True
        elif matrix[x+1][y] == (x,y) and matrix[x][y+1] == (x+1,y+1):
            #print("horizontal merge")
            matrix[x+1][y] = (x+1, y+1)
            matrix[x][y+1] = (x, y)
            return True
        elif matrix[x][y] == (x,y+1) and matrix[x+1][y+1] == (x+1,y):
            #print("vertical merge")
            matrix[x][y] = (x+1, y)
            matrix[x+1][y+1] = (x, y+1)
            return True 
        elif matrix[x][y+1] == (x,y) and matrix[x+1][y] == (x+1,y+1):
            #print("vertical merge")
            matrix[x][y+1] = (x+1, y+1)
            matrix[x+1][y] = (x, y)
            return True 
        else:
            return False