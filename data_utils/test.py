import os
import json
import torch
from scipy.io import loadmat
import json

anns = {
    '1': 123,
    '2': 234,
    '3': 123
}

ids = [1,2,3]

t = [anns[str(i)] for i in ids]

print(t)