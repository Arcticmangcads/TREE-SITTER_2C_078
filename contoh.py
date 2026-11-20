import os
from pathlib import Path

def tambah(a, b):
    """Menjumlahkan dua angka."""
    return a + b

def kali(a, b, c=1):
    print(a, b)
    return a * b * c

def halo():
    print("halo")

class Kalkulator:
    def bagi(self, x, y):
        return x / y