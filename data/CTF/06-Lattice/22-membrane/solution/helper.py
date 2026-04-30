import numpy as np


with np.load("data.npz") as f:
    pk_A = f["pk_A"]
    pk_b = f["pk_b"]
    encrypt_A = f["encrypt_A"]
    encrypt_b = f["encrypt_b"]
