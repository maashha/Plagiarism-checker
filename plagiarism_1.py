import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from keyword import iskeyword
import token
import tokenize
import zipfile
np.random.seed(0)
sns.set_theme()
tokens_list = []
filename = 'Архив_2.zip'
with zipfile.ZipFile(filename) as zip:
    namelist = zip.namelist()
number_files = len(namelist)
# проводим токенизацию кода
# для каждого слова кода определяем является он строкой, числом и т.д.
# каждый отдельный тип слов обозначаем своим символом 
# после анализа всего кода получаем строку, состоящую из этим символов
for files in range(0, number_files, 2):
    with zipfile.ZipFile('Архив_2.zip') as thezip:
        with tokenize.open(namelist[files]) as f:
            tokens = tokenize.generate_tokens(f.readline)
            finalToken = ''
            for token in tokens:
                if token[0] == 53:
                    finalToken = finalToken+'O'
                elif token[0] == 2:
                    finalToken = finalToken+'N'
                elif token[1] == 'for' or token[1] == 'while':
                    finalToken = finalToken+'C'
                elif iskeyword(token[1]) is True:
                    finalToken = finalToken+'K'
                elif token[1] == 'list' or token[1] == 'dict':
                    finalToken = finalToken+'V'
                elif token[1] == 'tuple' or token[1] == 'set':
                    finalToken = finalToken+'V'
                elif token[1] == 'bool' or token[1] == 'str':
                    finalToken = finalToken+'V'
                elif token[1] == 'int':
                    finalToken = finalToken+'V'
                elif token[0] == 1:
                    finalToken = finalToken+'I'
            tokens_list.append(finalToken)


# сравниваем каждые две строки по алгоритму Фишера
def fisher(word1, word2):
    comparison = [0] * (len(word2)+1)
    for element in range(len(word2)+1):
        comparison[element] = [0] * (len(word1)+1)
    for line in range(len(word2)+1):
        for column in range(len(word1)+1):
            if line == 0:
                comparison[line][column] = column
            elif column == 0:
                comparison[line][column] = line
    for line in range(1, len(word2)+1):
        for column in range(1, len(word1)+1):
            if word2[line-1] == word1[column-1]:
                comparison[line][column] = min(comparison[line][column-1]+1,
                                               comparison[line-1][column]+1,
                                               comparison[line-1][column-1])
            else:
                comparison[line][column] = min(comparison[line][column-1]+1,
                                               comparison[line-1][column]+1,
                                               comparison[line-1][column-1]+1)
    return (1-(comparison[len(word2)][len(word1)]/max(len(word1),
               len(word2))))*100
# создаем массив, в котором будут находиться итоговые значения попарных сранений
resoults = []
lines = []
for number_name in range(number_files//2):
    if number_name != 0:
        resoults.append(lines)
    lines = []
    for name_number in range(number_files//2):
        lines.append(100)
resoults.append(lines)
# выводим результаты для каждых двух сравнимаемых программ
for first_file in range(number_files//2):
    for second_file in range(first_file+1, number_files//2):
        if fisher(tokens_list[first_file], tokens_list[second_file]):
            print(namelist[first_file*2], namelist[second_file*2],
                  fisher(tokens_list[first_file], tokens_list[second_file]))
        # добавляем значения процента схожести в массивы с результатами
        resoults[first_file][second_file] = fisher(tokens_list[first_file],
                                                   tokens_list[second_file])
        resoults[second_file][first_file] = fisher(tokens_list[first_file],
                                                   tokens_list[second_file])
# делаем из массива с результатами DataFrame
# по его данным строим heatmap
DataFrame_resoults = pd.DataFrame(resoults)
sns.heatmap(DataFrame_resoults, cmap="ocean",  vmin=0, vmax=100)
plt.show()
