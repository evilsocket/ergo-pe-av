import logging as log

from keras.callbacks import EarlyStopping

# define training strategy
def train_model(model, dataset):
    log.info("training model (train on %d samples, validate on %d) ..." % ( \
            len(dataset.Y_train), 
            len(dataset.Y_val) ) )
    
    loss      = 'binary_crossentropy'
    optimizer = 'adam'
    metrics   = ['accuracy']
    
    model.compile(loss = loss, optimizer = optimizer, metrics = metrics)

    earlyStop = EarlyStopping(monitor = 'val_acc', min_delta=0.0001, patience = 5, mode = 'auto')
    return model.fit( dataset.X_train, dataset.Y_train,
            batch_size = 64,
            epochs = 50,
            verbose = 2,
            validation_data = (dataset.X_val, dataset.Y_val),
            callbacks = [earlyStop])