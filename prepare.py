import os
import sys

import logging as log
import numpy as np
import pandas as pd
import werkzeug.datastructures

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import encoder

def prepare_names():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "attribute.names")
    log.info("creating %s" % path)
    with open(path, 'w+t') as fp:
        for name in encoder.attribute_names():
            fp.write("%s\n" % name)


def prepare_dataset(filename):
    prepare_names()
    data = pd.read_csv(filename, sep = ',', header = None)
    return data.replace(encoder.classes)

def prepare_input(x, is_encoding = False):
    # file upload
    if isinstance(x, werkzeug.datastructures.FileStorage):
        return encoder.encode_pe(x)
    # file path
    elif len(x) > 0 and x[0] == '/':
        return encoder.encode_pe(x)
    # raw vector
    else:
        return x.split(',')


