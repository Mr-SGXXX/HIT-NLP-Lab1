# 实验一第四部分 - 基于机械匹配的分词系统的速度优化
import time


# class TrieTree:
#     def __init__(self):
#         self.root = [None] * HASH_ARRAY_SIZE
#
#     def add_word(self, word):
#         child, node_list = self.get_child_with(word[0])
#         if child is None:
#             if node_list is None:
#                 self.root[hash_letter(word[0], HASH_ARRAY_SIZE)] = [TrieNode(word)]
#             else:
#                 node_list.append(TrieNode(word))
#         else:
#             child.add_child(word)
#         # try:
#         #     index = self.root.index(word[0])
#         #     self.root[index + 1].add_child(word)
#         # except ValueError:
#         #     self.root.append(word[0])
#         #     self.root.append(TrieNode(word))
#
#     def get_child_with(self, character):
#         node_list = self.root[hash_word(character, HASH_ARRAY_SIZE)]
#         if node_list is None:
#             return None, None
#         for node in node_list:
#             if node.character == character:
#                 return node, node_list
#         return None, node_list
#
#     def get_child(self, word):
#         i = 0
#         child, node_list = self.get_child_with(word[0])
#         if child is None:
#             return None
#         while i != len(word) - 1:
#             i += 1
#             child, node_list = child.get_child_with(word[i])
#             if child is None:
#                 return None
#         return child
#
#     def have_word(self, word):
#         i = 0
#         child, node_list = self.get_child_with(word[0])
#         if child is None:
#             return False
#         # cur_node = self.root[hash_word(word[i], HASH_ARRAY_SIZE)]
#         # try:
#         #     index = self.root.index(word[i])
#         #     cur_node = self.root[index + 1]
#         # except ValueError:
#         #     return False
#         while i != len(word) - 1:
#             i += 1
#             child, node_list = child.get_child_with(word[i])
#             if child is None:
#                 return False
#         return child.is_terminal()
#
#
# class TrieNode:
#     def __init__(self, left_letters):
#         self.character = left_letters[0]
#         # self.children = []
#         self.children = [None] * HASH_ARRAY_SIZE
#         if len(left_letters) != 1:
#             self.terminal_flag = False
#             self.children[hash_letter(left_letters[1], HASH_ARRAY_SIZE)] = [TrieNode(left_letters[1:])]
#             # try:
#             #     index = self.children.index(left_letters[1])
#             #     self.children[index + 1].add_child(left_letters[1:])
#             # except ValueError:
#             #     self.children.append(left_letters[1])
#             #     self.children.append(TrieNode(left_letters[1:]))
#         else:
#             self.terminal_flag = True
#
#     def add_child(self, left_letters):
#         if len(left_letters) != 1:
#             child, node_list = self.get_child_with(left_letters[1])
#             if child is None:
#                 if node_list is None:
#                     self.children[hash_letter(left_letters[1], HASH_ARRAY_SIZE)] = [TrieNode(left_letters[1:])]
#                 else:
#                     node_list.append(TrieNode(left_letters[1:]))
#             else:
#                 child.add_child(left_letters[1:])
#             # try:
#             #     index = self.children.index(left_letters[1])
#             #     self.children[index + 1].add_child(left_letters[1:])
#             # except ValueError:
#             #     self.children.append(left_letters[1])
#             #     self.children.append(TrieNode(left_letters[1:]))
#         else:
#             self.terminal_flag = True
#
#     def is_terminal(self):
#         return self.terminal_flag
#
#     def get_child_with(self, character):
#         node_list = self.children[hash_letter(character, HASH_ARRAY_SIZE)]
#         if node_list is None:
#             return None, None
#         for node in node_list:
#             if node.character == character:
#                 return node, node_list
#         return None, node_list
#         # try:
#         #     index = self.children.index(character)
#         #     return self.children[index + 1]
#         # except ValueError:
#         #     return None
#
#     def __str__(self):
#         return '字符：' + str(self.character)

class TrieNode:
    # 构造函数
    def __init__(self, character, terminal, children):
        self.character = character
        self.terminal = terminal
        self.children = children

    # 返回当前节点Terminal
    def is_terminal(self):
        return self.terminal

    # 设置当前节点Terminal
    def set_terminal(self, terminal):
        self.terminal = terminal

    # 获得当前节点字符
    def get_character(self):
        return self.character

    # 设置当前节点字符
    def set_character(self, character):
        self.character = character

    # 获取当前节点的子节点
    def get_children(self):
        return self.children

    # 获取指定的一个子节点
    def get_child(self, character):
        index = hash_letter(character, HASH_ARRAY_SIZE)
        while self.children[index] is not None and self.children[index].character != character:
            index += 1
        return self.children[index]
        # if character not in self.children:
        #     return None
        # return self.children[character]

    def get_child_if_not_exist_then_create(self, character):
        child = self.get_child(character)
        if not child:
            child = TrieNode(character, False, [None] * HASH_ARRAY_SIZE)
            # child = TrieNode(character, False, {})
            self.add_child(child)
        return child

    def add_child(self, child):
        index = hash_letter(child.character, HASH_ARRAY_SIZE)
        while self.children[index] is not None:
            index += 1
        self.children[index] = child
        # self.children[child.character] = child

    def remove_child(self, child):
        index = hash_letter(child.character, HASH_ARRAY_SIZE)
        while self.children[index] is not None and self.children[index] != child:
            index += 1
        self.children[index] = None
        # self.children[child.character] = None
def contain(word):
    word = word.replace(" ", "")
    if len(word) < 1:
        return False
    node = Root_node
    for i in word:
        child = node.get_child(i)
        if not child:
            return False
        else:
            node = child
    return node.is_terminal()

def add(word):
    word = word.replace(" ", "")
    if len(word) < 1:
        return
    node = Root_node

    for i in word:
        child = node.get_child_if_not_exist_then_create(i)
        node = child
    node.set_terminal(True)


DATA_PATH = "./res/199801_sent.txt"
DICT_PATH = "./res/dic.txt"
TIME_COST_PATH = "./res/TimeCost.txt"
HASH_ARRAY_SIZE = 10000

Max_len = 0
Dict = []
Dict_accelerate = None
Accelerate_flag = False
# Trie_tree = TrieTree()
# Root_node = TrieNode("", False, {})
Root_node = TrieNode("", False, [None] * HASH_ARRAY_SIZE)

def hash_letter(letter, array_size):
    return (3 * ord(letter) + 5) % array_size


def hash_word(word, array_size):
    hash_code = 1
    for i in word:
        hash_code = (hash_code * 3 * ord(i) + 5) % array_size
    return hash_code


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
                # Trie_tree.add_word(part[0])
                add(part[0])
            if len(part[0]) > Max_len:
                Max_len = len(part[0])
            line = dict_file.readline()
    dict_file.close()


def word_in_dict(try_word):
    global Root_node
    return contain(try_word)


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
    # Time_start = time.time()
    # with open(DATA_PATH, 'r') as Data_file:
    #     Line = Data_file.readline()
    #     while Line != '':
    #         Rst_FMM = FMM(Line.strip('\n'))
    #         # Origin_file.write(Rst_FMM + '\n')
    #         Line = Data_file.readline()
    # Time_end = time.time()
    # Time_cost_file.write("未加速FMM用时： " + str(Time_end - Time_start) + "s\n")
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
    # New_file.close()
