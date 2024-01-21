from os import listdir
from moviepy.editor import *

month_path = r"D:\website\backend\data"
input_list = ['AFTERNOON','BOY','GIRL']
list_data = listdir(month_path)
nWords = len(input_list)
i = 0
while i < nWords:
    input_word = input_list[i].upper()
    for file in list_data:
        file_words = file[:-4].split(" ")
        if input_word == file_words[0]:
            file_path = month_path + "\\" + file
            VideoFileClip(file_path).preview(fps=30)
            i += len(file_words)
            break
    else:
        i += 1
