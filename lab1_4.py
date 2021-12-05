# 实验一第四部分 - 基于机械匹配的分词系统的速度优化
import time
from lab1_5.utils import pre_process


class TrieTree:
    def __init__(self):
        self.root = [None] * HASH_ARRAY_SIZE

    def add_word(self, word):
        child, node_list = self.get_child_with(word[0])
        if child is None:
            if node_list is None:
                self.root[hash_letter(word[0], HASH_ARRAY_SIZE)] = [TrieNode(word)]
            else:
                node_list.append(TrieNode(word))
        else:
            child.add_child(word)

    def get_child_with(self, character):
        node_list = self.root[hash_word(character, HASH_ARRAY_SIZE)]
        if node_list is None:
            return None, None
        for node in node_list:
            if node.character == character:
                return node, node_list
        return None, node_list

    def get_child(self, word):
        i = 0
        child, node_list = self.get_child_with(word[0])
        if child is None:
            return None
        while i != len(word) - 1:
            i += 1
            child, node_list = child.get_child_with(word[i])
            if child is None:
                return None
        return child

    def have_word(self, word):
        i = 0
        child, node_list = self.get_child_with(word[0])
        if child is None:
            return False
        while i != len(word) - 1:
            i += 1
            child, node_list = child.get_child_with(word[i])
            if child is None:
                return False
        return child.is_terminal()


class TrieNode:
    def __init__(self, left_letters):
        self.character = left_letters[0]
        self.children = [None] * HASH_ARRAY_SIZE
        if len(left_letters) != 1:
            self.terminal_flag = False
            self.children[hash_letter(left_letters[1], HASH_ARRAY_SIZE)] = [TrieNode(left_letters[1:])]
        else:
            self.terminal_flag = True

    def add_child(self, left_letters):
        if len(left_letters) != 1:
            child, node_list = self.get_child_with(left_letters[1])
            if child is None:
                if node_list is None:
                    self.children[hash_letter(left_letters[1], HASH_ARRAY_SIZE)] = [TrieNode(left_letters[1:])]
                else:
                    node_list.append(TrieNode(left_letters[1:]))
            else:
                child.add_child(left_letters[1:])
        else:
            self.terminal_flag = True

    def is_terminal(self):
        return self.terminal_flag

    def get_child_with(self, character):
        node_list = self.children[hash_letter(character, HASH_ARRAY_SIZE)]
        if node_list is None:
            return None, None
        for node in node_list:
            if node.character == character:
                return node, node_list
        return None, node_list

    def __str__(self):
        return '字符：' + str(self.character)


DATA_PATH = "./res/199801_sent.txt"
DICT_PATH = "./res/dic.txt"
TIME_COST_PATH = "./res/TimeCost.txt"
HASH_ARRAY_SIZE = 10007

Max_len = 0
Dict = []
Dict_accelerate = None
Accelerate_flag = False
Trie_tree = TrieTree()


def hash_letter(letter, array_size):
    return (ord(letter) + 5) % array_size


def hash_word(word, array_size):
    hash_code = 1
    for i in word:
        hash_code = (hash_code * ord(i) + 5) % array_size
    return hash_code


def load_dict(dict_path):
    global Dict, Max_len
    with open(dict_path, 'r') as dict_file:
        line = dict_file.readline()
        while line != '':
            part = line.split(":")
            Dict.append(part[0])
            if len(part[0]) > Max_len:
                Max_len = len(part[0])
            line = dict_file.readline()


def load_dict_accelerate(dict_path):
    global Accelerate_flag, Dict_accelerate, Trie_tree, Max_len
    Accelerate_flag = True
    dict_file = open(dict_path, 'r')
    line = dict_file.readline()
    while line != '':
        part = line.split(":")
        if len(part[0]) != 1:
            Trie_tree.add_word(part[0])
        if len(part[0]) > Max_len:
            Max_len = len(part[0])
        line = dict_file.readline()
    dict_file.close()


def FMM(line):
    rst = ""
    while len(line) > 0:
        cur_len = Max_len if Max_len < len(line) else len(line)
        # try_word = line[:cur_len]
        try_word = line[len(line) - cur_len:]
        while cur_len > 1:
            processed_word = pre_process(try_word)
            if not Accelerate_flag and processed_word not in Dict:
                try_word = try_word[:len(try_word) - 1]
            elif Accelerate_flag and not Trie_tree.have_word(processed_word):
                # try_word = try_word[:len(try_word) - 1]
                try_word = try_word[1:]
            else:
                break
            cur_len -= 1
        rst = rst + try_word + '/ '
        # line = line[len(try_word):]
        line = line[:len(line) - len(try_word)]
    return rst


if __name__ == "__main__":
    load_dict(DICT_PATH)
    Time_cost_file = open(TIME_COST_PATH, 'w')
    # Time_start = time.time()
    # with open(DATA_PATH, 'r') as Data_file:
    #     Line = Data_file.readline()
    #     while Line != '':
    #         FMM(Line.strip('\n'))
    #         Line = Data_file.readline()
    # Time_end = time.time()
    # Time_cost_file.write("未加速FMM用时： " + str(Time_end - Time_start) + "s\n")
    load_dict_accelerate(DICT_PATH)
    a = open("./res/seg_BMM1.txt", "w")
    Time_start = time.time()
    with open(DATA_PATH, 'r') as Data_file:
        Line = Data_file.readline()
        while Line != '':
            a.write(FMM(Line.strip('\n')) + "\n")
            Line = Data_file.readline()
    Time_end = time.time()
    Time_cost_file.write("加速后FMM用时： " + str(Time_end - Time_start) + "s\n")
    Time_cost_file.close()
    a.close()
