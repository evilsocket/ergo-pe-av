import logging as log

from keras.models import Sequential
from keras.layers import Dense, Dropout

# used by `ergo train <path>` to build the model structure
def build_model(is_train):  
    # our model is a simple ANN with 486 inputs, two hidden
    # layers of 70 neurons each, dropout of 30% while training
    # and two output classes (0=clean 1=malicious)
    n_inputs = 486
    log.info("building model for %s ..." % 'training' if is_train else 'evaluation')
    if is_train:
        return Sequential([
            Dense(70, input_shape=(n_inputs,), activation='relu'),
            Dropout(0.3),
            Dense(70, activation='relu'),
            Dropout(0.3),
            Dense(2, activation='softmax')
        ])
    else:
        return Sequential([
            Dense(70, input_shape=(n_inputs,), activation='relu'),
            Dense(70, activation='relu'),
            Dense(2, activation='softmax')
        ])
