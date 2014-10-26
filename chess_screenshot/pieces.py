import png
import sys
import os
import chess.pgn
import chess
import glob

class Board(object):
    def __init__(self, rows):
        self.rows = rows
        self.w = len(rows[0])/3
        self.orientation = ""
                
        # Convert to greyscale
        greyboard = []
        for row in rows:
            greyrow = []
            summ = 0
            n = 1
            
            for val in row:
                summ = summ + val
                if n % 3 == 0:
                    greyrow.append(summ/3)
                    summ = 0
                n = n + 1
            greyboard.append(list(greyrow))
        
        #print "board size in pixels"
        #print len(greyboard)
        #print len(greyboard[0])
          
        self.g = greyboard
        
        squareWidth = self.w / 8
        
        #print "square width in pixel"
        #print squareWidth
        
        # Create individual squares
        self.squares = []
        numSquares = 0  
        x = 0
        numRows = 0
        # we ll take them in this order: top to bottom, left to right
        # a bit messy . it works but beeds to check
        while numRows < 8:
            numCols = 0
            y = 0
            while numCols < 8:
                pixVals = []
                
                for arow in range(y,y+squareWidth):
                    for acol in range(x,x+squareWidth):
                        pixVals.append(self.g[arow][acol])
                
                self.squares.append(Square(numRows, numCols, squareWidth, list(pixVals), self))
                numSquares += 1
                numCols += 1
                y = y+squareWidth
            numRows += 1
            x = x+squareWidth
            
        self.orientation = self.squares[0].find_ori()
        
    def to_pgn_game(self):
        game = chess.pgn.Game()        
        bitboard = chess.Bitboard()
        
        for sq in self.squares:
            if sq.piece != "":
                bitboard.set_piece_at(sq.coord(), sq.fpiece())
                
        game.setup(bitboard)
        return game
        
    def export_pgn(self, filename):
        with open(filename, "w") as new_pgn:
            game = self.to_pgn_game()
            exporter = chess.pgn.FileExporter(new_pgn)
            game.export(exporter)
        
        print "Created %s" % (filename)
    
    @classmethod
    def from_filename(cls, filename):
        r = png.Reader(filename)
        x = r.read()
        pixels = x[2]
        
        # board is at 188th row and has a height of 480        
        num = 0
        board = []
        for i in pixels:
            if num >= 187 and num < 667:
                board.append(i)
            num = num + 1
                
        return cls(board)


class Square(object):
    def __init__(self, x, y, w, pixels, parent):
        self.piece = "none"
        self.w = w
        self.pixels = pixels
        self.x = x
        self.y = y
        self.color = ""
        self.av = 0
        self.pcode = 0
        self.ccode = 0
        self.orientation = ""
        self.parent = parent
        
        self.rows = []
        row = []
        count = 0
        for xx in self.pixels:
            row.append(xx)
            count = count+1
            if count == 60:
                self.rows.append(list(row))
                row = []
                count = 0
        
        self.identify()
    
    def find_ori(self):
        if 10 > self.w:
            return ""
        
        summ = 0
        num = 0
        for x in range(2,10):
            for y in range(2,10):
                summ += self.rows[y][x]
                num += 1
        av = summ / num
        
        if av < 170:
            self.orientation = "1down"
            return "1down"
        else:
            self.orientation = "1up"
            return "1up"
         
        
                
    def coord(self):
        if self.parent.orientation == "1up":
            xs = [7, 6, 5, 4, 3, 2, 1, 0]
            return chess.SQUARES[xs[self.x] + self.y * 8]
        else:
            ys = [7, 6, 5, 4, 3, 2, 1, 0]
            return chess.SQUARES[self.x + ys[self.y] * 8]
            
    
    def fpiece(self):
        return chess.Piece(self.pcode, self.ccode)
    
    def identify(self):
        #print "Square ", self.x+1, self.y+1
        
        #average method
        # not used anymore but can be useful maybe for other purposes
        av = sum(self.pixels)/len(self.pixels)
        self.av = av
        
        
        myrow = self.pixels[self.w*self.w/2+5:self.w/2*self.w+self.w-5]
        #print myrow
        #num cpnsecutive white at the middle horizontal line
        num_wcons = 0
        max_wcons = 0
        num_wzons = 0
        wz = []
        in_zone = False
        for val in myrow:
            if val > 215:
                num_wcons +=1
                in_zone = True
            else:
                if num_wcons > 2:
                    if num_wcons > max_wcons:
                        max_wcons = num_wcons
                    if in_zone:
                        num_wzons += 1
                        wz.append(num_wcons)
                in_zone = False
                num_wcons = 0
                
        #print "wcons ", max_wcons, " wzons ", num_wzons, wz
        
        # conclusions based on white stats
        if num_wzons != 0:
            self.color = "white"
            self.ccode = 0
            if num_wzons == 1:
                if max_wcons > 15:
                    self.piece = "rook"
                    self.pcode = chess.ROOK
                else:
                    self.piece = "pawn"
                    self.pcode = chess.PAWN
            elif num_wzons == 2:
                if wz[0]-wz[1] > 14:
                    self.piece = "bishop"
                    self.pcode = chess.BISHOP
                elif wz[0]-wz[1] > 7:
                    self.piece = "knight"
                    self.pcode = chess.KNIGHT
                else:
                    self.piece = "king"
                    self.pcode = chess.KING
            else:
                self.piece = "queen"
                self.pcode = chess.QUEEN
                    
        
        #num cpnsecutive blacks at the middle horizontal line
        num_bcons = 0
        max_bcons = 0
        num_bzons = 0
        bz = []
        in_zone = False
        for val in myrow:
            if val < 130 and val > 100:
                num_bcons +=1
                in_zone = True
            else:
                if num_bcons > 2:
                    if in_zone and num_bcons > 2:
                        num_bzons += 1
                        bz.append(num_bcons)
                    max_bcons = max(max_bcons, num_bcons)
                in_zone = False
                num_bcons = 0
                
        #print "bcons ", max_bcons, " bzons ", num_bzons, bz
        
        # conclusions based on black stats
        if num_bzons != 0:
            self.color = "black"
            self.ccode = 1
            if num_bzons == 1:
                if max_bcons > 15:
                    self.piece = "rook"
                    self.pcode = chess.ROOK
                else:
                    self.piece = "pawn"
                    self.pcode = chess.PAWN
            elif num_bzons == 2:
                if bz[0]-bz[1] > 14:
                    self.piece = "bishop"
                    self.pcode = chess.BISHOP
                elif bz[0]-bz[1] > 7:
                    self.piece = "knight"
                    self.pcode = chess.KNIGHT
                else:
                    self.piece = "king"
                    self.pcode = chess.KING
            else:
                self.piece = "queen"
                self.pcode = chess.QUEEN
    
    def __repr__(self):
        x=  "%d %d %s %s" % (self.x+1, self.y+1, str(self.color), str(self.piece))
        return x
            
def process_one_file(filename):
    print "Processing %s" % (filename)

    myboard = Board.from_filename(filename)    
    directory = os.path.dirname(filename)
    basename = os.path.splitext(filename)[0]
    myboard.export_pgn('%s.pgn' % (basename))
        
if __name__ == '__main__':
    
    #print sys.argv
    
    if len(sys.argv) != 2:
        print "usage : pieces.py filepath/filename.png"
        sys.exit(0)
    
    filename = sys.argv[1]
    if (os.path.isfile(filename)) == False and (os.path.isdir(filename)) == False:
        print "%s is not a valid file" % (filename)
        sys.exit(0)
    
    if (os.path.isfile(filename)) == True:
        process_one_file(filename)
    else: 
        #directiory 
        for file in os.listdir(filename):
            if file.endswith(".png"):
                process_one_file(os.path.join(filename,file))
                
                
    print "DONE"
        
    
    