# T-Rex Genetic
AI teaches  itself to play a simplifed version of the popular chrome game (T-Rex) by  playing randomly and trying to pass down the good characteristics to the new generation of T-Rexs
 
#### Preview
##### Video
 [![IMAGE ALT TEXT](http://img.youtube.com/vi/PMCXyKOWDSs/0.jpg)](https://www.youtube.com/watch?v=PMCXyKOWDSs)
 
 ![alt text](https://raw.githubusercontent.com/Hiasat/trex-genetic-deeplearning/master/with_birds.png)

#### Breif Techinical overview:
There might be other ways to make an AI for this game but I used Genetics as a cool experiment, it starts by initlizating many random neural network, I found out that there is a linear correlation between variables ,so my nueral network architecture is 3 inputs (game-speed,obstacle type,obstacle distance) and 1 output (Sigmoid Activiation Function) which represents jumping or not
jumping
Algorithms Steps
- Let new generation play the game
- Evaluate each gnommes by giving fitness score
- Crossover between top gnomes
- Mutate them
- Repeat!
 
#### CrossOver
I tried  a couple of crossovers , the one I am using is either keep using same main gentics , or take average of both parents.
#### Mutate
I multiply the weights in the neural network by a random change rate .
#### Fitness Score
I am using the ratio between the number of obstacles it jumped over and the number of times space was pressed multiplied by game score , the reason I used the ratio is to eliminate jumpers gnomes.
 
#### Source files
- brain.py contains learning algorithm
- main.py contains game
- constant.py contains contsant variables
 
#### Todos
 - Do more analyzing to make sure it always converges to the optimal solution.
 - Do better randomization
 
#### Libraries used
- Tensorflow 
- Pygame
- Numpy
#### References
- https://github.com/shivamshekhar/Chrome-T-Rex-Rush
