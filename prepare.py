import os
import sys

import logging as log
import numpy as np
import pandas as pd

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

def prepare_input(filename, is_encoding = False):
    return encoder.encode_pe(filename)
