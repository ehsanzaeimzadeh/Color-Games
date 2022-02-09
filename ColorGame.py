from tkinter import *
import random
# Created by @EhsanZaeimzadeh <ehsan@pigmentory.app>
__author__ = "Ehsan Zaeimzadeh"
__email__ = "ehsan@pigmentory.app"
class ColorGame():
   def __init__(self, cellWidth, cellNumber):
      self.mainWindow = Tk()
      self.mainWindow.wm_title("Color Game")
      self.frameWidth = cellWidth*cellNumber
      self.cellWidth = cellWidth
      self.cells = {}
      self.colors = ["brown", "blue", "yellow", "green", "orange", "red"]
      self.iterIndex = 0

      self.markedCells = ["C"+str(self.cellWidth)+"R"+str(self.cellWidth)]
      self.nrOfMarkedCells_old = len(self.markedCells)
      self.nrOfMarkedCells_new = 0

      self.topFrame = Frame(bd = 4, relief = GROOVE)
      self.botFrame = Frame(bd = 4, relief = GROOVE)
      self.logFrame = Frame(bd = 4, relief = GROOVE)
      self.topFrame.pack()
      self.botFrame.pack()
      self.logFrame.pack()

      self.gameBoard = Canvas(self.topFrame, width = self.frameWidth+self.cellWidth,
                              height = self.frameWidth+self.cellWidth)
      self.gameBoard.pack()

      for col in range(0, self.frameWidth+self.cellWidth, self.cellWidth):
         for row in range(0, self.frameWidth+self.cellWidth, self.cellWidth):
            if col == 0 or row == 0 or col == self.frameWidth or row == self.frameWidth:
               self.cells["C"+str(col)+"R"+str(row)] = self.gameBoard.create_rectangle(col, row,
                                                                                      col+self.cellWidth,
                                                                                      row+self.cellWidth,
                                                                                      fill = "black")
            else:
               thisColor = self.colors[random.randint(0, len(self.colors)-1)]
               self.cells["C" + str(col) + "R" + str(row)] = self.gameBoard.create_rectangle(col, row,
                                                                                            col + self.cellWidth,
                                                                                            row + self.cellWidth,
                                                                                            fill=thisColor)

      Button(self.botFrame, text=" "*10, bg="brown",  command=lambda: self.fillColor("brown") ).grid(row=0, column=0)
      Button(self.botFrame, text=" "*10, bg="blue",   command=lambda: self.fillColor("blue")  ).grid(row=0, column=1)
      Button(self.botFrame, text=" "*10, bg="yellow", command=lambda: self.fillColor("yellow")).grid(row=0, column=2)
      Button(self.botFrame, text=" "*10, bg="red",    command=lambda: self.fillColor("red")   ).grid(row=0, column=3)
      Button(self.botFrame, text=" "*10, bg="green",  command=lambda: self.fillColor("green") ).grid(row=0, column=4)
      Button(self.botFrame, text=" "*10, bg="orange", command=lambda: self.fillColor("orange")).grid(row=0, column=5)
      Button(self.botFrame, text="New Game!", command=self.newGame).grid(row=0, column=len(self.colors))

      self.log = Text(self.logFrame, height = 20)
      self.log.pack()
      log = "*"*40 + "\nNew game: " + str(cellNumber-1) + "x" + str(cellNumber-1) +"\n"
      self.log.insert(END, log)
      self.log.config(state=DISABLED)

      self.getNumberOfeachColor()
      mainloop()

   # -------------------------------------------------------------------------------------------------------------------
   def fillColor(self, color):
      self.nrOfMarkedCells_old = len(self.markedCells)
      self.iterIndex += 1
      self.enterLog("\n-----\nIteration#: {}\n".format(self.iterIndex))
      oldColor = self.getColor(self.getCellName(self.cellWidth, self.cellWidth))
      currentCells = self.markedCells
      for cellName in currentCells:
         for neighbor in self.findNeighbors(cellName):
            if oldColor == self.getColor(neighbor):
               try:
                  self.markedCells.index(neighbor)
               except ValueError:
                  self.markedCells.append(neighbor)

      for cellName in self.markedCells:
         self.gameBoard.itemconfig(self.cells[cellName], fill = color)
      self.nrOfMarkedCells_new = len(self.markedCells)

      self.enterLog("NrOf Cells with changed color: {}\n".format(self.nrOfMarkedCells_new - self.nrOfMarkedCells_old))
      self.enterLog("Total nr of new coloredCells: {}\n".format(self.nrOfMarkedCells_new))
      self.getStatistics()
      self.getNumberOfeachColor()

   # -------------------------------------------------------------------------------------------------------------------
   def getColor(self, cellName):
      return self.gameBoard.itemcget(self.cells[cellName], "fill")

   # -------------------------------------------------------------------------------------------------------------------
   def getCellName(self, col, row):
      return "C"+str(col)+"R"+str(row)

   # -------------------------------------------------------------------------------------------------------------------
   def getStatistics(self):
      colorCounts = {"brown": 0, "blue": 0, "yellow": 0, "green": 0, "orange": 0, "red": 0}
      neighborList = []
      for cellName in self.markedCells:
         for neighbor in self.findNeighbors(cellName):
            if "black" not in self.getColor(neighbor):
               neighborList.append(neighbor)
      newNeighborList = set([x for x in neighborList if x not in self.markedCells])
      for neighbor in newNeighborList:
         colorCounts[self.getColor(neighbor)] += 1

      log = ""
      for color in colorCounts.keys():
         log += color + ": " + str(colorCounts[color]) + "\n"
      self.enterLog(log)

   #-------------------------------------------------------------------------------------------------------------------
   def getNumberOfeachColor(self):
      colorCounts = {"brown": 0, "blue": 0, "yellow": 0, "green": 0, "orange": 0, "red": 0}
      for cellName in self.cells.keys():
         if "black" not in self.getColor(cellName):
            colorCounts[self.getColor(cellName)] += 1

      log = "--------------------------\n"
      for color in colorCounts.keys():
         log += color + ": " + str(colorCounts[color]) + "\n"

      self.enterLog(log)

   # -------------------------------------------------------------------------------------------------------------------
   def findNeighbors(self, cellName):
      col = int(cellName.split("R")[0][1:])
      row = int(cellName.split("R")[1])
      return (["C"+str(col-self.cellWidth)+"R"+str(row),
               "C"+str(col)+"R"+str(row-self.cellWidth),
               "C"+str(col)+"R"+str(row+self.cellWidth),
               "C"+str(col+self.cellWidth)+"R"+str(row)])

   # -------------------------------------------------------------------------------------------------------------------
   def newGame(self):
      self.markedCells = ["C" + str(self.cellWidth) + "R" + str(self.cellWidth)]
      for cellName in self.cells.keys():
         if not("R0" in cellName or "C0" in cellName or ("R"+str(self.frameWidth)) in cellName or ("C"+str(self.frameWidth)) in cellName):
            self.gameBoard.itemconfig(self.cells[cellName], fill = self.colors[random.randint(0, len(self.colors)-1)])
      self.enterLog("*"*40 + "\nNew game: " + str((self.frameWidth/self.cellWidth)-1) + "x" + str((self.frameWidth/self.cellWidth)-1) +"\n")
      self.iterIndex = 0

   # -------------------------------------------------------------------------------------------------------------------
   def enterLog(self, log):
      self.log.config(state=NORMAL)
      self.log.insert(END, log)
      self.log.config(state=DISABLED)


newGame = ColorGame(20, 11)
