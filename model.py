import logging as log

from keras.models import Sequential
from keras.layers import Dense, Dropout

def build_model(is_train):  
    n_inputs = 486
    log.info("building model for %s ..." % 'training' if is_train else 'evaluation')
    # only add dropout for training
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
