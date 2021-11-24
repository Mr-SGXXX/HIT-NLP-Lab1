# 实验一第一部分 - 词典的构建

DICT = {}
WORD_LEN_MAP = {}
DATA_PATH_LIST = ["./res/199801_seg&pos.txt"]
DICT_PATH = "./res/dic.txt"
MAX_WORD_LEN = 0
TOTAL_WORD_NUM = 0
Long_word = ""

def load_by_line(string):
    global TOTAL_WORD_NUM, DICT, WORD_LEN_MAP, MAX_WORD_LEN, Long_word
    word_list = string.split()
    long_word_flag = False
    for word in word_list:
        parts = word.split("/")
        if parts[0][0] == '[':
            long_word_flag = True
            parts[0] = parts[0][1:]
            Long_word += parts[0]
        elif long_word_flag and parts[1].__contains__(']'):
            Long_word += parts[0]
            word_c = parts[1].split(']')
            parts[1] = word_c[0]
            if not DICT.__contains__(Long_word):
                if len(Long_word) > MAX_WORD_LEN:
                    MAX_WORD_LEN = len(Long_word)
                if not WORD_LEN_MAP.__contains__(len(Long_word)):
                    WORD_LEN_MAP[len(Long_word)] = [Long_word]
                else:
                    WORD_LEN_MAP[len(Long_word)].append(Long_word)
                DICT[Long_word] = [word_c[1], 1]
            elif not DICT[Long_word].__contains__(word_c[1]):
                DICT[Long_word].append(word_c[1])
                DICT[Long_word].append(1)
            else:
                i = DICT[Long_word].index(word_c[1]) + 1
                DICT[Long_word][i] += 1
            TOTAL_WORD_NUM += 1
            Long_word = ""
            long_word_flag = False
        elif long_word_flag:
            Long_word += parts[0]
        if not DICT.__contains__(parts[0]):
            if len(parts[0]) > MAX_WORD_LEN:
                MAX_WORD_LEN = len(parts[0])
            if not WORD_LEN_MAP.__contains__(len(parts[0])):
                WORD_LEN_MAP[len(parts[0])] = [parts[0]]
            else:
                WORD_LEN_MAP[len(parts[0])].append(parts[0])
            DICT[parts[0]] = [parts[1], 1]
        elif not DICT[parts[0]].__contains__(parts[1]):
            DICT[parts[0]].append(parts[1])
            DICT[parts[0]].append(1)
        else:
            i = DICT[parts[0]].index(parts[1]) + 1
            DICT[parts[0]][i] += 1
        TOTAL_WORD_NUM += 1


def output_dict():
    global DICT, WORD_LEN_MAP, MAX_WORD_LEN
    dict_file = open(DICT_PATH, "w")
    i = 0
    for j in range(MAX_WORD_LEN):
        if WORD_LEN_MAP.get(j):
            dict_file.write(str(j) + '\n')
            for key in WORD_LEN_MAP.get(j):
                line = key + ":"
                for value in DICT[key]:
                    if i % 2 == 0:
                        line += value + " "
                        i = 1
                    else:
                        line += str(value / TOTAL_WORD_NUM) + " "
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
