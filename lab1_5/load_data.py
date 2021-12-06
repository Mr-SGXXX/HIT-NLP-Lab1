# 加载数据部分
from utils import pre_process
from Trie import TrieTree
import numpy as np

Dict_Trie = TrieTree()
Prefix_Trie = TrieTree(False)
Pos_Label_Map = ['st', 'ed']
Pos_Num_Map = {}
Total_Word_Num = 0
State_Trans_Mat = np.zeros((50, 50))


def smooth_plus1():
    global State_Trans_Mat, Pos_Label_Map
    pass


def smooth_good_turing():
    global State_Trans_Mat, Pos_Label_Map
    pass


def smooth_katz():
    global State_Trans_Mat, Pos_Label_Map
    pass


def load_test(part, part_num, raw_data_path, true_data_path):
    line_num = -1
    raw_lines = []
    with open(raw_data_path, 'r') as data_file:
        line = data_file.readline()
        line_num += 1
        while line != '':
            if line_num % part_num == part or part == -1:
                raw_lines.append(line.strip('\n'))
            line = data_file.readline()
            line_num += 1
    line_num = -1
    true_lines = []
    with open(true_data_path, 'r') as data_file:
        line = data_file.readline()
        line_num += 1
        while line != '':
            if line_num % part_num == part or part == -1:
                true_lines.append(line.strip('\n'))
            line = data_file.readline()
            line_num += 1
    return raw_lines, true_lines


def load_dict(part, part_num, data_path_list, smooth_func=None):
    """
    载入数据
    :param part: k折时不取的第k折
    :param part_num: 折数
    :param data_path_list: 数据路径
    :param smooth_func: 参数平滑函数
    :return: 前缀树、词性顺序、词性出现数目、总词数、状态转移矩阵
    """
    global Dict_Trie, Prefix_Trie, Pos_Label_Map, Pos_Num_Map, Total_Word_Num, State_Trans_Mat
    line_num = -1
    Pos_Num_Map['st'] = 0
    Pos_Num_Map['ed'] = 0
    for data_path in data_path_list:
        with open(data_path, 'r') as data_file:
            line = data_file.readline()
            line_num += 1
            while line != '':
                if line_num % part_num != part or part == -1:
                    load_by_line(line.strip('\n'))
                line = data_file.readline()
                line_num += 1
    for i in range(len(Pos_Label_Map)):
        State_Trans_Mat[i] /= Pos_Num_Map[Pos_Label_Map[i]]
    if smooth_func is not None:
        smooth_func()
    return Dict_Trie, Prefix_Trie, Pos_Label_Map, Pos_Num_Map, Total_Word_Num, State_Trans_Mat


def load_by_line(line):
    global Dict_Trie, Prefix_Trie, Pos_Label_Map, Pos_Num_Map, Total_Word_Num, State_Trans_Mat
    word_list = line.split()
    long_word_flag = False
    parts = None
    for i in range(len(word_list)):
        if i == 0:
            Pos_Num_Map['st'] += 1
            pre_pos = 'st'
        elif i == 1 and pre_process(parts[0]) == "\\linePosition":
            pre_pos = 'st'
        else:
            pre_pos = parts[1]
        word = word_list[i]
        parts = word.split("/")
        if parts[0][0] == '[':
            long_word_flag = True
            parts[0] = parts[0][1:]
        elif long_word_flag and parts[1].__contains__(']'):
            word_c = parts[1].split(']')
            parts[1] = word_c[0]
            long_word_flag = False
        Dict_Trie.add_word(parts[0], parts[1])
        Prefix_Trie.add_word(parts[0], parts[1])
        Total_Word_Num += 1
        if i == 0 and pre_process(parts[0]) == "\\linePosition":
            continue
        if parts[1] not in Pos_Label_Map:
            Pos_Label_Map.append(parts[1])
        if parts[1] not in Pos_Num_Map:
            Pos_Num_Map[parts[1]] = 1
        else:
            Pos_Num_Map[parts[1]] += 1
        i = Pos_Label_Map.index(pre_pos)
        j = Pos_Label_Map.index(parts[1])
        State_Trans_Mat[i, j] += 1
    if parts is not None:
        i = Pos_Label_Map.index(parts[1])
        j = 1
        State_Trans_Mat[i, j] += 1
        Pos_Num_Map['ed'] += 1
