import os
import logging as log

from keras.callbacks import EarlyStopping, ModelCheckpoint

# define training strategy
def train_model(model, dataset):
    log.info("training model (train on %d samples, validate on %d) ..." % ( \
            len(dataset.Y_train), 
            len(dataset.Y_val) ) )
    
    loss      = 'binary_crossentropy'
    optimizer = 'adam'
    metrics   = ['accuracy']
    
    model.compile(loss = loss, optimizer = optimizer, metrics = metrics)

    checkpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkpoints")
    os.makedirs(checkpath, exist_ok=True)
    checkpath = os.path.join(checkpath, 'model-epoch{epoch:03d}-acc{val_acc:03f}.h5')

    # this will stop the training when the validation accuracy will stop changing
    stopper = EarlyStopping(monitor = 'val_acc', min_delta=0.0001, patience = 5, mode = 'auto')
    # this will take snapshots of the best performing epoch
    saver = ModelCheckpoint(checkpath, save_best_only=True, verbose=1, monitor='val_loss', mode='min')
    # start training
    return model.fit( dataset.X_train, dataset.Y_train,
            batch_size = 64,
            epochs = 50,
            verbose = 2,
            validation_data = (dataset.X_val, dataset.Y_val),
            callbacks = [saver, stopper])
