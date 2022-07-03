import snake
import brain

shouldTrain = input("Do you want to train brain? (Y/N):  ")
win = brain.SnakeAIWindow("testBrain", shouldTrain=="Y")
while win._game.isAlive():
    win.step()
win.stop()
