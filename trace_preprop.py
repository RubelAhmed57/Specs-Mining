from collections import *
from itertools import permutations as pm
import time, os
import re,csv

with open('1.tstt.txt') as file:
    file_contents = file.read()
    file_contents = re.findall('-?\d+', file_contents)

f= open("1.tstt_pr.txt","w+")
for number in file_contents:
    f.write(str(int(number))+"\t")
f.close()