# 实验一第二部分 - 正反向最大匹配分词实现

DATA_PATH = "./res/199801_sent.txt"
DICT_PATH = "./res/dic.txt"
SEG_FMM_PATH = "./res/seg_FMM.txt"
SEG_BMM_PATH = "./res/seg_BMM.txt"
DICT = []
MAX_LEN = 0


def load_dict(dict_path):
    global DICT, MAX_LEN
    with open(dict_path, 'r') as dict_file:
        lines = dict_file.readlines()
        for line in lines:
            part = line.split(":")
            DICT.append(part[0])
            MAX_LEN = max(len(part[0]), MAX_LEN)


def FMM(line):
    rst = ""
    while len(line) > 0:
        min_len = min(MAX_LEN, len(line))
        try_word = line[:min_len]
        for cur_len in range(min_len, 1, -1):
            if try_word in DICT:
                break
            try_word = try_word[:len(try_word) - 1]
        rst = rst + try_word + '/ '
        line = line[len(try_word):]
    return rst


def BMM(line):
    rst = ""
    while len(line) > 0:
        min_len = min(MAX_LEN, len(line))
        try_word = line[len(line) - min_len:]
        for cur_len in range(min_len, 1, -1):
            if try_word in DICT:
                break
            try_word = try_word[1:]
        rst = try_word + '/ ' + rst
        line = line[:len(line) - len(try_word)]
    return rst


if __name__ == "__main__":
    load_dict(DICT_PATH)
    with open(DATA_PATH, 'r') as Data_file, \
            open(SEG_FMM_PATH, 'w') as Out_FMM_file, open(SEG_BMM_PATH, 'w') as Out_BMM_file:
        Line = Data_file.readline()
        while Line != '':
            Rst_FMM = FMM(Line.strip('\n'))
            Rst_BMM = BMM(Line.strip('\n'))
            Out_FMM_file.write(Rst_FMM + '\n')
            Out_BMM_file.write(Rst_BMM + '\n')
            Line = Data_file.readline()
