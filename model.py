import logging as log

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout

def build_model(is_train):  
    n_inputs       = 486
    n_hidden       = (70, 70,)
    dropout        = 0.3
    activation     = 'relu'
    out_activation = 'softmax'
  
    log.info("building model for %s ..." % 'training' if is_train else 'evaluation')

    model = Sequential()
    for i, n_neurons in enumerate(n_hidden):
        # setup the input layer
        if i == 0:
            model.add(Dense(n_neurons, input_shape = (n_inputs,), activation = activation))
        else:
            model.add(Dense(n_neurons, activation = activation))
        # add dropout
        if is_train:
            model.add(Dropout(dropout))
    # setup output layer
    model.add(Dense(2, activation = out_activation))
    
    return model
