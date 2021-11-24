# 实验一第四部分 - 基于机械匹配的分词系统的速度优化
import time


class DoubleTrieTree:
    def __init__(self):
        pass

    def have_word(self, word):
        pass


class TrieTreeState:
    def __init__(self):
        pass


DATA_PATH = "./res/199801_sent.txt"
DICT_PATH = "./res/dic.txt"
TIME_COST_PATH = "./res/TimeCost.txt"

Max_len = 0
Dict = []
Dict_accelerate = None
Accelerate_flag = False


def load_dict(dict_path):
    global Dict, Max_len
    with open(dict_path, 'r') as dict_file:
        line = dict_file.readline()
        last_len = 0
        while line != '':
            try:
                length = int(line)
                while last_len != length:
                    Dict.append([])
                    last_len += 1
                line = dict_file.readline()
            except ValueError:
                part = line.split(":")
                Dict[length - 1].append(part[0])
                if len(part[0]) > Max_len:
                    Max_len = len(part[0])
                line = dict_file.readline()


def load_dict_accelerate(dict_path):
    global Accelerate_flag, Dict_accelerate
    Accelerate_flag = True
    pass


def word_in_dict(try_word):
    return False


def FMM(line):
    rst = ""
    while len(line) > 0:
        cur_len = Max_len if Max_len < len(line) else len(line)
        try_word = line[:cur_len]
        while cur_len > 1:
            if not Accelerate_flag and try_word not in Dict[cur_len - 1]:
                try_word = try_word[:len(try_word) - 1]
            elif Accelerate_flag and word_in_dict(try_word):
                try_word = try_word[:len(try_word) - 1]
            else:
                break
            cur_len -= 1
        rst = rst + try_word + '/ '
        line = line[len(try_word):]
    return rst


if __name__ == "__main__":
    load_dict(DICT_PATH)
    Time_cost_file = open(TIME_COST_PATH, 'w')
    Time_start = time.time()
    with open(DATA_PATH, 'r') as Data_file:
        Line = Data_file.readline()
        while Line != '':
            Rst_FMM = FMM(Line.strip('\n'))
            Line = Data_file.readline()
    Time_end = time.time()
    Time_cost_file.write("未加速FMM用时： " + str(Time_end - Time_start) + "s\n")
    load_dict_accelerate(DICT_PATH)
    Time_start = time.time()
    with open(DATA_PATH, 'r') as Data_file:
        Line = Data_file.readline()
        while Line != '':
            Rst_FMM = FMM(Line.strip('\n'))
            Line = Data_file.readline()
    Time_end = time.time()
    Time_cost_file.write("加速后FMM用时： " + str(Time_end - Time_start) + "s\n")
    Time_cost_file.close()
