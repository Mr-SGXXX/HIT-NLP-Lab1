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
    global State_Trans_Mat, Pos_Label_Map, Pos_Num_Map, Total_Word_Num
    pos_num = len(Pos_Label_Map)
    mat = State_Trans_Mat[:pos_num, :pos_num]
    for i in range(pos_num):
        for j in range(pos_num):
            mat[i, j] += 1
            Pos_Num_Map[Pos_Label_Map[j]] += 1
            Total_Word_Num += 1


def smooth_plusP():
    global State_Trans_Mat, Pos_Label_Map, Pos_Num_Map, Total_Word_Num
    pos_num = len(Pos_Label_Map)
    mat = State_Trans_Mat[:pos_num, :pos_num]
    for i in range(pos_num):
        Pos_Num_Map[Pos_Label_Map[i]] += pos_num
    Total_Word_Num += pos_num * pos_num
    for i in range(pos_num):
        for j in range(pos_num):
            if mat[i, j] == 0:
                mat[i, j] = Pos_Num_Map[Pos_Label_Map[j]] / Total_Word_Num


def load_test(part, part_num, raw_data_path, true_data_path):
    """
    加载测试数据
    :param part: K折，选取的折数， -1时表示全部选取
    :param part_num: 折数
    :param raw_data_path: 待分词数据文件路径
    :param true_data_path: 正确分词数据文件路径
    :return: 待分词数据，正确分词数据
    """
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


def load_dict(part, part_num, data_path_list, folded_data_list, name_path, smooth_func=smooth_plus1):
    """
    载入数据
    :param part: k折时不取的第k折
    :param part_num: 折数
    :param data_path_list: 数据路径
    :param folded_data_list: 需要K折的文件序号
    :param name_path 人名词典路径
    :param smooth_func: 参数平滑函数
    :return: 前缀树、词性顺序、词性出现数目、总词数、状态转移矩阵
    """
    global Dict_Trie, Prefix_Trie, Pos_Label_Map, Pos_Num_Map, Total_Word_Num, State_Trans_Mat
    line_num = -1
    Pos_Num_Map['st'] = 0
    Pos_Num_Map['ed'] = 0
    seq = 0
    for data_path in data_path_list:
        seq += 1
        with open(data_path, 'r') as data_file:
            line = data_file.readline()
            line_num += 1
            while line != '':
                if line_num % 2500 == 0:
                    print("已读取行数：" + str(line_num))
                if (line_num % part_num != part or part == -1) and seq in folded_data_list:
                    load_by_line(line.strip('\n'))
                if seq not in folded_data_list:
                    load_by_line(line.strip('\n'))
                line = data_file.readline()
                line_num += 1
        load_name(name_path)
    smooth_func()
    return Dict_Trie, Prefix_Trie, Pos_Label_Map, Pos_Num_Map, Total_Word_Num, State_Trans_Mat


def load_name(name_path):
    global Total_Word_Num, Pos_Num_Map
    with open(name_path, 'r', encoding='utf-8') as name_file:
        line = name_file.readline().strip("\n")
        if len(line) == 2 or len(line) == 3:
            Dict_Trie.add_word(line[0], 'nr')
            Prefix_Trie.add_word(line[0], 'nr')
            Dict_Trie.add_word(line[1:], 'nr')
            Prefix_Trie.add_word(line[1:], 'nr')
            Total_Word_Num += 2
            Pos_Num_Map['nr'] += 2
        elif len(line) == 4:
            Dict_Trie.add_word(line[:1], 'nr')
            Prefix_Trie.add_word(line[:1], 'nr')
            Dict_Trie.add_word(line[2:], 'nr')
            Prefix_Trie.add_word(line[2:], 'nr')
            Total_Word_Num += 2
            Pos_Num_Map['nr'] += 2


def save_weights(weight_path):
    global Dict_Trie, Prefix_Trie, Pos_Label_Map, Pos_Num_Map, Total_Word_Num, State_Trans_Mat
    with open(weight_path, 'w') as weight_file:
        weight_file.write(str(Total_Word_Num) + '\n')
        for label in Pos_Label_Map:
            weight_file.write(str(label) + ' ')
        weight_file.write('\n')
        for key in Pos_Num_Map:
            weight_file.write(str(key) + ':' + str(Pos_Num_Map[key]) + " ")
        weight_file.write('\n')
        for i in range(50):
            for j in range(50):
                weight_file.write(str(State_Trans_Mat[i, j]) + ' ')
        weight_file.write('\n')
        Dict_Trie.save_trie(weight_file)
        Prefix_Trie.save_trie(weight_file)


def load_weights(weight_path):
    with open(weight_path, 'r') as weight_file:
        line = weight_file.readline().strip('\n')
        total_word_num = int(line)
        line = weight_file.readline().strip('\n')
        pos_label_map = []
        parts = line.split()
        for part in parts:
            pos_label_map.append(part)
        line = weight_file.readline().strip('\n')
        pos_num_map = {}
        parts = line.split()
        for part in parts:
            pos, num = part.split(':')
            pos_num_map[pos] = int(num)
        line = weight_file.readline().strip('\n')
        state_trans_mat = np.zeros((50, 50))
        parts = line.split()
        for i in range(50):
            for j in range(50):
                state_trans_mat[i][j] = parts[i * 50 + j]
        dict_trie = TrieTree()
        dict_trie.load_trie(weight_file)
        prefix_trie = TrieTree()
        prefix_trie.load_trie(weight_file)
    return dict_trie, prefix_trie, pos_label_map, pos_num_map, total_word_num, state_trans_mat


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
