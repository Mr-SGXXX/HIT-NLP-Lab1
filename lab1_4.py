# 实验一第四部分 - 基于机械匹配的分词系统的速度优化
import time


class TrieTree:
    def __init__(self):
        self.root = []

    def add_word(self, word):
        try:
            index = self.root.index(word[0])
            self.root[index + 1].add_child(word)
        except ValueError:
            self.root.append(word[0])
            self.root.append(TrieNode(word))

    def have_word(self, word):
        i = 0
        try:
            index = self.root.index(word[i])
            cur_node = self.root[index + 1]
        except ValueError:
            return False
        while i != len(word) - 1:
            i += 1
            cur_node = cur_node.get_child_with(word[i])
            if cur_node is None:
                return False
        return cur_node.is_terminal()


class TrieNode:
    def __init__(self, left_letters):
        self.character = left_letters[0]
        self.children = []
        if len(left_letters) != 1:
            self.terminal_flag = False
            try:
                index = self.children.index(left_letters[1])
                self.children[index + 1].add_child(left_letters[1:])
            except ValueError:
                self.children.append(left_letters[1])
                self.children.append(TrieNode(left_letters[1:]))
        else:
            self.terminal_flag = True

    def add_child(self, left_letters):
        if len(left_letters) != 1:
            try:
                index = self.children.index(left_letters[1])
                self.children[index + 1].add_child(left_letters[1:])
            except ValueError:
                self.children.append(left_letters[1])
                self.children.append(TrieNode(left_letters[1:]))
        else:
            self.terminal_flag = True

    def is_terminal(self):
        return self.terminal_flag

    def get_child_with(self, character):
        try:
            index = self.children.index(character)
            return self.children[index + 1]
        except ValueError:
            return None


DATA_PATH = "./res/199801_sent.txt"
DICT_PATH = "./res/dic.txt"
TIME_COST_PATH = "./res/TimeCost.txt"

Max_len = 0
Dict = []
Dict_accelerate = None
Accelerate_flag = False
Trie_tree = TrieTree()


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
    global Accelerate_flag, Dict_accelerate, Trie_tree, Max_len
    Accelerate_flag = True
    dict_file = open(dict_path, 'r')
    line = dict_file.readline()
    while line != '':
        try:
            int(line)
            line = dict_file.readline()
        except ValueError:
            part = line.split(":")
            if len(part[0]) != 1:
                Trie_tree.add_word(part[0])
            if len(part[0]) > Max_len:
                Max_len = len(part[0])
            line = dict_file.readline()
    dict_file.close()


def word_in_dict(try_word):
    global Trie_tree
    return Trie_tree.have_word(try_word)


def FMM(line):
    rst = ""
    while len(line) > 0:
        cur_len = Max_len if Max_len < len(line) else len(line)
        try_word = line[:cur_len]
        while cur_len > 1:
            if not Accelerate_flag and try_word not in Dict[cur_len - 1]:
                try_word = try_word[:len(try_word) - 1]
            elif Accelerate_flag and not word_in_dict(try_word):
                try_word = try_word[:len(try_word) - 1]
            else:
                break
            cur_len -= 1
        rst = rst + try_word + '/ '
        line = line[len(try_word):]
    return rst


if __name__ == "__main__":
    load_dict(DICT_PATH)
    # Origin_file = open("./res/origin_MM.txt", 'w')
    # New_file = open("./res/new_MM.txt", 'w')
    Time_cost_file = open(TIME_COST_PATH, 'w')
    Time_start = time.time()
    with open(DATA_PATH, 'r') as Data_file:
        Line = Data_file.readline()
        while Line != '':
            Rst_FMM = FMM(Line.strip('\n'))
            # Origin_file.write(Rst_FMM + '\n')
            Line = Data_file.readline()
    Time_end = time.time()
    Time_cost_file.write("未加速FMM用时： " + str(Time_end - Time_start) + "s\n")
    load_dict_accelerate(DICT_PATH)
    Time_start = time.time()
    with open(DATA_PATH, 'r') as Data_file:
        Line = Data_file.readline()
        while Line != '':
            Rst_FMM = FMM(Line.strip('\n'))
            # New_file.write(Rst_FMM + '\n')
            Line = Data_file.readline()
    Time_end = time.time()
    Time_cost_file.write("加速后FMM用时： " + str(Time_end - Time_start) + "s\n")
    Time_cost_file.close()
    # Origin_file.close()
    # New_file

