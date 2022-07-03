from os.path import exists
import random
import numpy as np
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter

import snake as s


def rotateClockwise(vec):
    return np.array([vec[1], -vec[0]])
def rotateAnticlockwise(vec):
    return np.array([-vec[1], vec[0]])


class SnakeBrain:
    def __init__(self, shouldTrain, boardSize: int, filename: str, learningRate: float, trainingGames: int, maxTrainingSteps: int, minimumTrainingScore: int):
        network = input_data(shape=[None, 4, 1], name='input')
        network = fully_connected(network, 25)
        network = fully_connected(network, 8)
        network = fully_connected(network, 3, activation='softmax')
        network = regression(network, optimizer='adam', learning_rate=learningRate, loss='mean_square', name='targets')
        self._model = tflearn.DNN(network)

        self._filename = filename

        hasTrained = False
        if exists(filename+".meta"):
            self._loadTrainedModel()
            hasTrained = True
        else:
            print("No previous save of "+filename+" was found, creating new brain")
        
        if shouldTrain:
            self._trainModel(hasTrained, boardSize, trainingGames, maxTrainingSteps, minimumTrainingScore)
            

    def _trainModel(self, hasTrained, boardSize, trainingGames, maxTrainingSteps, minimumTrainingScore):
        ## Create training data ##
        trainingData = []
        successfulGames = 0
        for i in range(trainingGames):
            game = s.SnakeGame(boardSize)
            snake, apple = game.getGameObjects()

            gameHistory = []
            distanceScore = 20
            prevDist = 100000
            
            for j in range(maxTrainingSteps):
                #Save observation/inputs
                distToApple, inputs = self.generateBrainInputs(game)

                if distToApple < prevDist:
                    distanceScore += 5
                elif distToApple > prevDist:
                    distanceScore -= 6
                prevDist = distToApple
                
                #Generate an action
                shouldBeRandom = (not hasTrained) or (random.randint(0,1)==0)
                action = 0
                if shouldBeRandom: #random action
                    action = random.randint(0,2)
                else: #action from previous brain
                    action = np.argmax(self._model.predict(inputs.reshape(-1, 4, 1)))
                
                #Change direction
                direction = snake.getDirection()
                if action == 1:
                    snake.setDirection(rotateAnticlockwise(direction))
                elif action == 2:
                    snake.setDirection(rotateClockwise(direction))
                    #Action 0 = forward, action 1 = left, action 2 = right
                outputs = np.array([int(action==0), int(action==1), int(action==2)])

                #proceed game
                game.step()

                if game.isAlive and distanceScore > 0:
                    gameHistory.append([inputs,outputs])
                else:
                    break

            #Check if min training score is achieved
            if game.getScore()+distanceScore/2 >= minimumTrainingScore:
                successfulGames += 1
                for data in gameHistory:
                    trainingData.append(data)
        print(str(successfulGames)+" successful games!")

        ## Train the model ##
        X = np.array([i[0] for i in trainingData]).reshape(-1, 4, 1)
        y = np.array([i[1] for i in trainingData]).reshape(-1, 3)
        self._model.fit(X, y, n_epoch=3, shuffle=True, run_id=self._filename)
        self._model.save(self._filename)
                

    def _loadTrainedModel(self):
        self._model.load(self._filename)


    def generateBrainInputs(self, game):
        snake, apple = game.getGameObjects()
        #snake blocked?
        direction = snake.getDirection()
        frontBlocked = game.isSnakeBlocked(direction)
        leftBlocked = game.isSnakeBlocked(rotateAnticlockwise(direction))
        rightBlocked = game.isSnakeBlocked(rotateClockwise(direction))
        #apple
        dirToApple = apple.getPos()-snake.getHead()
        distToApple = np.sqrt(dirToApple.dot(dirToApple))
        angleToApple = direction.dot(dirToApple)
        if distToApple != 0:
            angleToApple/distToApple
            if rotateAnticlockwise(direction).dot(dirToApple)/distToApple < 0:
                #If the angle is closer to the right of the snake, then angle is negative
                angleToApple *= -1
        #distToApple = distToApple/game.getSize() #Make distance relative
        return distToApple, np.array([int(frontBlocked), int(leftBlocked), int(rightBlocked), angleToApple])

    def generateBrainDecision(self, game):
        _, inputs = self.generateBrainInputs(game)
        prediction = self._model.predict(inputs.reshape(-1, 4, 1))
        return np.argmax(prediction)


class SnakeAIWindow(s.SnakeWindow):
    def __init__(self, filename, shouldTrain):
        learningRate = float(input("Learning rate?:  "))
        trainingGames = int(input("How many training games?:  "))
        minScore = int(input("Minimum score?:  "))
        super().__init__()
        self._brain = SnakeBrain(shouldTrain, self._size, filename, learningRate, trainingGames, 250, minScore)

    def step(self):
        chosenAction = self._brain.generateBrainDecision(self._game)
        snake, apple = self._game.getGameObjects()
        direction = snake.getDirection()
        if chosenAction == 1:
            snake.setDirection(rotateAnticlockwise(direction))
        elif chosenAction == 2:
            snake.setDirection(rotateClockwise(direction))

        self._game.step()
        super().step()        
