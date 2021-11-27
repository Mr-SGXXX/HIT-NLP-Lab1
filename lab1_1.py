# 实验一第一部分 - 词典的构建
from utils import pre_process

DICT = {}
PROPERTY_MAP = {}
DATA_PATH_LIST = ["./res/199801_seg&pos.txt"]
DICT_PATH = "./res/dic.txt"
MAX_WORD_LEN = 0


def load_by_line(string):
    global DICT, MAX_WORD_LEN, PROPERTY_MAP
    word_list = string.split()
    long_word_flag = False
    for word in word_list:
        parts = word.split("/")
        if parts[0][0] == '[':
            long_word_flag = True
            parts[0] = parts[0][1:]
        elif long_word_flag and parts[1].__contains__(']'):
            word_c = parts[1].split(']')
            parts[1] = word_c[0]
            long_word_flag = False
        parts[0] = pre_process(parts[0])
        if not DICT.__contains__(parts[0]):
            if len(parts[0]) > MAX_WORD_LEN:
                MAX_WORD_LEN = len(parts[0])
            DICT[parts[0]] = [parts[1], 1]
        elif not DICT[parts[0]].__contains__(parts[1]):
            DICT[parts[0]].append(parts[1])
            DICT[parts[0]].append(1)
        else:
            i = DICT[parts[0]].index(parts[1]) + 1
            DICT[parts[0]][i] += 1
        if parts[1] not in PROPERTY_MAP:
            PROPERTY_MAP[parts[1]] = 1
        else:
            PROPERTY_MAP[parts[1]] += 1


def output_dict():
    global DICT, PROPERTY_MAP
    dict_file = open(DICT_PATH, "w")
    i = 0
    for word in DICT:
        line = word + ":"
        for value in DICT[word]:
            if i % 2 == 0:
                line += value + " "
                num = PROPERTY_MAP[value]
                i = 1
            else:
                line += str(value / num) + " "
                i = 0
        dict_file.write(line + '\n')
    dict_file.close()


if __name__ == "__main__":
    for Data_path in DATA_PATH_LIST:
        Data_file = open(Data_path, 'r')
        Str = Data_file.readline()
        while Str != '':
            load_by_line(Str)
            Str = Data_file.readline()
        Data_file.close()
    output_dict()
