import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import encoder

def prepare_dataset(filename):
    data = pd.read_csv(filename, sep = ',', header = None)
    return data.replace(encoder.classes)

def prepare_input(filename, is_encoding = False):
    return encoder.encode_pe(filename)
