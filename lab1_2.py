# 实验一第二部分 - 正反向最大匹配分词实现

DATA_FILE = "./res/199801_sent.txt"
DICT_PATH = "./res/dic.txt"
SEG_FMM_PATH = "./res/seg_FMM.txt"
SEG_BMM_PATH = "./res/seg_BMM.txt"

DICT = []
MAX_LEN = 0
# LONGEST_STR = ''


def load_dict(dict_path):
    global DICT, MAX_LEN, LONGEST_STR
    dict_file = open(dict_path, 'r')
    line = dict_file.readline()
    while line != '':
        part = line.split(":")
        DICT.append(part[0])
        if len(part[0]) > MAX_LEN:
            MAX_LEN = len(part[0])
            # LONGEST_STR = part[0]
        # DICT.append(part[1].split()[::2])
        line = dict_file.readline()
    dict_file.close()


def FMM():
    pass


def BMM():
    pass


if __name__ == "__main__":
    load_dict(DICT_PATH)
    pass
