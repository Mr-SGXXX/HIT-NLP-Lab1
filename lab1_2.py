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
        line = dict_file.readline()
        last_len = 0
        while line != '':
            try:
                length = int(line)
                while last_len != length:
                    DICT.append([])
                    last_len += 1
                line = dict_file.readline()
            except ValueError:
                part = line.split(":")
                DICT[length - 1].append(part[0])
                if len(part[0]) > MAX_LEN:
                    MAX_LEN = len(part[0])
                line = dict_file.readline()


def FMM(line):
    rst = ""
    while len(line) > 0:
        cur_len = MAX_LEN if MAX_LEN < len(line) else len(line)
        try_word = line[:cur_len]
        while cur_len > 1:
            if try_word not in DICT[cur_len - 1]:
                try_word = try_word[:len(try_word) - 1]
            else:
                break
            cur_len -= 1
        rst = rst + try_word + '/ '
        line = line[len(try_word):]
    return rst


def BMM(line):
    rst = ""
    while len(line) > 0:
        cur_len = MAX_LEN if MAX_LEN < len(line) else len(line)
        try_word = line[len(line) - cur_len:]
        while cur_len > 1:
            if try_word not in DICT[cur_len - 1]:
                try_word = try_word[1:]
            else:
                break
            cur_len -= 1
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
