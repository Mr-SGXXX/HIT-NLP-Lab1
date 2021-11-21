# 实验一第一部分 - 词典的构建

DICT = {}
DATA_PATH_LIST = ["./res/199801_seg&pos.txt"]
DICT_PATH = "./res/dic.txt"

total_word_num = 0

def load_by_line(string):
    global total_word_num
    word_list = string.split()
    for word in word_list:
        parts = word.split("/")
        if not DICT.__contains__(parts[0]):
            DICT[parts[0]] = [parts[1], 1]
        elif not DICT[parts[0]].__contains__(parts[1]):
            DICT[parts[0]].append(parts[1])
            DICT[parts[0]].append(1)
        else:
            i = DICT[parts[0]].index(parts[1]) + 1
            DICT[parts[0]][i] += 1
        total_word_num += 1


def output_dict():
    dict_file = open(DICT_PATH, "w", encoding='utf-8')
    i = 0
    for key in DICT:
        line = key + ":"
        for value in DICT[key]:
            if i % 2 == 0:
                line += value + " "
                i = 1
            else:
                line += str(value / total_word_num) + " "
                i = 0
        dict_file.write(line + '\n')
    dict_file.close()


if __name__ == "__main__":
    for Data_path in DATA_PATH_LIST:
        Data_file = open(Data_path, 'r', encoding='utf-8')
        Str = Data_file.readline()
        while Str != '':
            Str = Data_file.readline()
            load_by_line(Str)
        Data_file.close()
    output_dict()

