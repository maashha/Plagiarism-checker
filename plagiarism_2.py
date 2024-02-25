import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from keyword import iskeyword
import token
import binascii
import tokenize
import zipfile
np.random.seed(0)
sns.set_theme()
tokens_list = []
filename = 'DIR.zip'
with zipfile.ZipFile(filename) as zip:
    namelist = zip.namelist()
number_files = len(namelist)

for files in range(0, number_files, 2):
    with zipfile.ZipFile('Архив_2.zip') as thezip:
        with tokenize.open(namelist[files]) as f:
            tokens = tokenize.generate_tokens(f.readline)
            token1 = ''
            for token in tokens:
                if token[0] == 53:
                    token1 = token1+'O'
                elif token[0] == 2:
                    token1 = token1+'N'
                elif token[1] == 'for' or token[1] == 'while':
                    token1 = token1+'C'
                elif iskeyword(token[1]) is True:
                    token1 = token1+'K'
                elif token[1] == 'list' or token[1] == 'dict':
                    token1 = token1+'V'
                elif token[1] == 'tuple' or token[1] == 'set':
                    token1 = token1+'V'
                elif token[1] == 'bool' or token[1] == 'str':
                    token1 = token1+'V'
                elif token[1] == 'int':
                    token1 = token1+'V'
                elif token[0] == 1:
                    token1 = token1+'I'
            tokens_list.append(token1)



def shingle(word):
    shingleLen = 4
    shingles = []
    for bit in range(len(word)-shingleLen+1):
        shingleSet = binascii.crc32(bytes(' '.join(word[bit:bit+shingleLen]),
                                          'utf-8'))
        shingles.append(shingleSet)
    return set(shingles)


def compare(shingles1, shingles2):
    same = 0
    for shingle in range(len(shingles1)):
        if shingles1[shingle] in shingles2:
            same = same + 1
    return same/(len(shingles1) + len(shingles2)-same)*100

resoults = []
lines = []
for number_name in range(number_files//2):
    if number_name != 0:
        resoults.append(lines)
    lines = []
    for name_number in range(number_files//2):
        lines.append(100)
resoults.append(lines)

for first_file in range(number_files//2):
    for second_file in range(first_file+1, number_files//2):
        if compare(list(shingle(tokens_list[first_file])),
                   list(shingle(tokens_list[second_file]))):
            finalPercent = compare(list(shingle(tokens_list[first_file])),
                        list(shingle(tokens_list[second_file])))
            print(namelist[first_file*2], namelist[second_file*2], finalPercent)
        
        resoults[first_file][second_file] = finalPercent
        resoults[second_file][first_file] = finalPercent

DataFrame_resoults = pd.DataFrame(resoults)
sns.heatmap(DataFrame_resoults, cmap="ocean",  vmin=0, vmax=100)
plt.show()
