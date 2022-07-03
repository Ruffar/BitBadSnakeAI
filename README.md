# What is this project for?

This just a small project for me to practice using TensorFlow and being comfortable with the basics of machine learning
WARNING: this project is unfinished and does not function properly yet

# Brain Overview

## Brain Inputs / Senses

The snake is able to sense:
- Whether something is in front, left, or right of the snake
- Angle between snake direction and snake to apple
(4 inputs)

From these inputs, the brain creates 3 outputs which determine whether it will move forward, left, or right

## Improvements to be made

- *Either restructure the neural network, train it more, or change how it's trained as it can't consistently get the apple
- Find a better reward system/picking of training data so that local maxima of snake moving in circles do not occur
- Make it so checking whether a direction is blocked (SnakeGame.isSnakeBlocked) is checked in one loop through entire snake instead of 3 loops of right, left, and forward

[* important]

## Learning Resources Used

[Article on Basic Snake Neural Network](https://towardsdatascience.com/today-im-going-to-talk-about-a-small-practical-example-of-using-neural-networks-training-one-to-6b2cbd6efdb3)

[Article on Using Tensorflow for Snake](https://tolotra.com/2018/02/23/tutorial-train-a-tensorflow-model-to-control-the-snake-game/)

[QnA on RELU](https://ai.stackexchange.com/questions/6468/why-do-we-prefer-relu-over-linear-activation-functions)

[Softmax Function Wikipedia](https://en.wikipedia.org/wiki/Softmax_function)