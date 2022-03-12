from tkinter import *
from Calibration import *
from DartsRecognition import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.minsize(width=800, height=600)
        self.pack()

class DartsScorer:
    currentPlayer = 1
    startScore = 501
    finalScore = 0
    playerOneScore = startScore
    playerTwoScore = startScore
    points = []

    calData_R = CalibrationData()
    calData_L = CalibrationData()

    def __init__(self, rightCam:VideoStream, leftCam:VideoStream):
        self.leftCamera = leftCam;
        self.rightCamera = rightCam;

    def calibrate(self):
        # calibrate cameras and safes calibration data
        self.calData_R, self.calData_L = calibrate(cam_R, cam_L)
        # take calibration frame
        success, cal_image = self.rightCamera.read()
        # save calibration frame
        cv2.imwrite("frame1.jpg", cal_image)

    def startGame(self):
        GUI.playerOneScoreEntry.configure(bg='light green')
        GUI.playerOneScoreEntry.delete(0, 'end')
        GUI.playerOneScoreEntry.insert(10, self.startScore)
        GUI.playerTwoScoreEntry.delete(0, 'end')
        GUI.playerTwoScoreEntry.insert(10, self.startScore)
        GUI.finalEntry.delete(0, 'end')
        for entry in GUI.entries:
            entry.delete(0, 'end')

        player.player = 1
        player.score = self.startScore
        # start getDart thread!!!
        self.startGetDartThread()

    def startGetDartThread(self):
        t = Thread(target=getDarts,
                   args=(self.rightCamera, self.leftCamera, self.calData_R, self.calData_L, player, GUI))
        t.start()

    def dartScores(self):
        # start motion processing in different thread, init scores
        if self.currentPlayer == 1:
            self.currentPlayer = 2
            GUI.playerTwoScoreEntry.configure(bg='light green')
            GUI.playerOneScoreEntry.configure(bg='white')
            score = int(GUI.playerTwoScoreEntry.get())
            player.player = self.currentPlayer
            player.score = score
        else:
            self.currentPlayer = 1
            GUI.playerOneScoreEntry.configure(bg='light green')
            GUI.playerTwoScoreEntry.configure(bg='white')
            score = int(GUI.playerOneScoreEntry.get())
            player.player = self.currentPlayer
            player.score = score

        # clear dartscores
        GUI.finalEntry.delete(0, 'end')
        for entry in GUI.entries:
            entry.delete(0, 'end')
        self.playerOneScore = int(GUI.playerOneScoreEntry.get())
        self.playerTwoScore = int(GUI.playerTwoScoreEntry.get())

        # start getDart thread!!!
        self.startGetDartThread()

    def correctLastDart(self):
        # correct dart score with binding -> press return to change
        # check if empty, on error write 0 to value of dart
        scoreSumOfEntries = 0
        for entry in GUI.entries:
            try:
                scoreSumOfEntries += int(eval(entry.get()))
            except:
                continue

        # check which player
        if self.currentPlayer == 1:
            new_score = self.playerOneScore - scoreSumOfEntries
            GUI.playerOneScoreEntry.delete(0, 'end')
            GUI.playerOneScoreEntry.insert(10, new_score)
        else:
            new_score = self.playerTwoScore - scoreSumOfEntries
            GUI.playerTwoScoreEntry.delete(0, 'end')
            GUI.playerTwoScoreEntry.insert(10, new_score)
        GUI.finalEntry.delete(0, 'end')
        GUI.finalEntry.insert(10, scoreSumOfEntries)


def createButtons():
    # Create Buttons
    calibrateButton = Button(None, text="Calibrate", fg="black", font="Helvetica 26 bold", command=dartScorer.calibrate())
    backgroundCanvas.create_window(20, 200, window=calibrateButton, anchor='nw')
    startGameButton = Button(None, text="Game On!", fg="black", font="Helvetica 26 bold", command=dartScorer.startGame())
    backgroundCanvas.create_window(20, 20, window=startGameButton, anchor='nw')
    quitButton = Button(None, text="QUIT", fg="black", font="Helvetica 26 bold", command=root.quit)
    backgroundCanvas.create_window(20, 300, window=quitButton, anchor='nw')
    nextPlayer = Button(None, text="Next Player", fg="black", font="Helvetica 26 bold", command=dartScorer.dartScores())
    backgroundCanvas.create_window(460, 400, window=nextPlayer, anchor='nw')

def createBackground():
    background = Canvas(root)
    background.pack(expand=True, fill='both')
    backgroundImage = PhotoImage(file="./Dartboard.gif")
    background.create_image(0, 0, anchor='nw', image=backgroundImage)
    return background

def createPlayerNameField(canvas:Canvas, name:str, x:int, y:int):
    entry = Entry(root, font="Helvetica 32 bold", width=7)
    canvas.create_window(x, y, window=entry, anchor='nw')
    entry.insert(10, name)

def createPlayerScoreField(canvas:Canvas, initialScore:int, x:int, y:int):
    entry = Entry(root, font="Helvetica 32 bold", width=7)
    canvas.create_window(x, y, window=entry, anchor='nw')
    entry.insert(10, str(initialScore))
    return entry

def createDartLabel(labelText:str, dartNumber:int, canvas:Canvas, offset:int):
    label = Label(None, text=labelText, font="Helvetica 20 bold")
    canvas.create_window(300, 160 + dartNumber * offset, window=label, anchor='nw')

def createDartEntryField(gui:GUIDef, dartScorer:DartsScorer, dartNumber:int, canvas:Canvas, offset:int):
    gui.entries[dartNumber] = Entry(root, font="Helvetica 20 bold", width=3)
    gui.entries[dartNumber].bind("<Return>", dartScorer.correctLastDart())
    canvas.create_window(350, 160 + dartNumber * offset, window=gui.entries[dartNumber], anchor='nw')

def createDartFields(gui:GUIDef, dartScorer:DartsScorer):
    yOffset: int = 50
    for dartNumber in range(3):
        createDartLabel(str(dartNumber + 1) + ".: ", dartNumber, canvas=backgroundCanvas, offset=yOffset)
        createDartEntryField(gui, dartScorer, dartNumber, canvas=backgroundCanvas, offset=yOffset)

def createFinalField(canvas:Canvas, gui:GUIDef):
    label = Label(None, text=" = ", font="Helvetica 20 bold")
    canvas.create_window(300, 310, window=label, anchor='nw')
    gui.finalEntry = Entry(root, font="Helvetica 20 bold", width=3)
    canvas.create_window(350, 310, window=gui.finalEntry, anchor='nw')


if __name__ == '__main__':
    root = Tk("OpenCV Dart")
    background = Canvas(root)
    background.pack(expand=True, fill='both')
    backgroundImage = PhotoImage(file="./Dartboard.gif")
    background.create_image(0, 0, anchor='nw', image=backgroundImage)

    for src in range(10):
        cam_R = VideoStream(camID=src)

    exit(0)
    """GUI = GUIDef()
    cam_R = VideoStream(src=2).start()
    cam_L = VideoStream(src=3).start()

    dartScorer = DartsScorer(cam_R, cam_L)


    # player = Player()

    backgroundCanvas = createBackground()
    createBackground()
    # createButtons()

    # createPlayerNameField(backgroundCanvas, "Player 1", 250, 20)
    # createPlayerNameField(backgroundCanvas, "Player 2", 400, 20)
    # GUI.playerOneScoreEntry = createPlayerScoreField(backgroundCanvas, dartScorer.startScore, 250, 80)
    # GUI.playerTwoScoreEntry = createPlayerScoreField(backgroundCanvas, dartScorer.startScore, 400, 80)

    # createDartFields(GUI)

    # createFinalField(backgroundCanvas, GUI)

    """
    app = Application(master=root)
    app.mainloop()
    root.destroy()
