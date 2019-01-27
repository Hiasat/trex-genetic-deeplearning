from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.optimizers import SGD
import constant
import numpy as np
import random
players_model = []
generation = 1

def create_model():
    model = Sequential()
    model.add(Dense(1, input_shape=(2,),activation='sigmoid'))
    #   model.add(Dense(NUMBER_OF_ACTIONS, activation='sigmoid'))
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss="mse", optimizer=sgd, metrics=["accuracy"])
    return model

def init():
    global players_model
    for player in range(0, constant.NUMBER_OF_DINO):
        #print("Setuping Player " + str(player))
        players_model.append(create_model())
        players_model[player]._make_predict_function()
def sigmoid(x):
    return (1 / (1 + np.exp(-x)))

def produce_new_generation(playersList):
    global  generation;
    generation = generation +1
    ############## Calculate FitnessScore
    for i in range(0, constant.NUMBER_OF_DINO):
        if playersList[i].jumps == 0:
            playersList[i].realScore = 0
        else:
            playersList[i].realScore = (playersList[i].jumpedOver / playersList[i].jumps) + 2 * sigmoid(playersList[i].score / 100);
        playersList.sort(key=lambda x: x.realScore, reverse=True)
    change_weights(0,playersList)

def change_weights(layer,playersList):
    new_weights = []
    for counter in range(0,constant.NUMBER_OF_DINO//2):
        idx_1 = playersList[random.randint(0,int(0.2*constant.NUMBER_OF_DINO))].realIdx
        idx_2 = playersList[random.randint(0,int(0.8*constant.NUMBER_OF_DINO))].realIdx
        new_weights1,new_weights2 = model_crossover(idx_1, idx_2,layer)
        updated_weights1 = model_mutate(new_weights1)
        updated_weights2 = model_mutate(new_weights2)
        new_weights.append(updated_weights1)
        new_weights.append(updated_weights2)
    global players_model
    for i in range(0,constant.NUMBER_OF_DINO):
        players_model[i].layers[layer].set_weights(new_weights[i])

def model_mutate(weights):
    for xi in range(len(weights)):
        for yi in range(len(weights[xi])):
            if (type(weights[xi][yi]) != np.float32):
                if random.uniform(0, 1) > 0.3:
                    change = random.uniform(-2,2)
                    weights[xi][yi] *= change
    return weights

def model_crossover(model_idx1, model_idx2,layer):
    global players_model
    weights1 = players_model[model_idx1].layers[layer].get_weights()
    weights2 = players_model[model_idx2].layers[layer].get_weights()
    weightsnew1 = weights1;
    weightsnew1[0] = (weights1[0]+weights2[0])*0.5;
    weightsnew2 = weights1
    return weightsnew1, weightsnew2

def jump(player_index,network_input):
    return players_model[player_index].predict(network_input, verbose=0) >= 0.5