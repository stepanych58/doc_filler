import os
from mainapp.mainapp.settings import *

for file in os.listdir(STATIC_DIR):
    if file:
        print(os.path.join(STATIC_DIR, file))