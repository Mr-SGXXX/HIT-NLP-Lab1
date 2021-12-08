from typing import Tuple, TextIO
from utils import pre_process, turn_zero


class TrieNode:
    def __init__(self, left_letters, part_of_speech):
        self.character = left_letters[0]
        self.children = {}
        self.pos_map = {}
        self.occur_time = 0
        if len(left_letters) != 1:
            self.terminal_flag = False
            self.children[left_letters[1]] = TrieNode(left_letters[1:], part_of_speech)
        else:
            self.pos_map[part_of_speech] = 1
            self.terminal_flag = True
            self.occur_time += 1

    def add_child(self, left_letters, part_of_speech):
        if len(left_letters) != 1:
            child = self.get_child_with(left_letters[1])
            if child is None:
                child = TrieNode(left_letters[1:], part_of_speech)
                self.children[left_letters[1]] = child
            else:
                child.add_child(left_letters[1:], part_of_speech)
        else:
            if part_of_speech not in self.pos_map:
                self.pos_map[part_of_speech] = 1
            else:
                self.pos_map[part_of_speech] += 1
            self.terminal_flag = True
            self.occur_time += 1

    def is_terminal(self):
        return self.terminal_flag

    def get_child_with(self, character):
        if character not in self.children:
            return None
        return self.children[character]

    def save_node(self, former_letters, file: TextIO):
        if self.terminal_flag:
            file.write(former_letters + self.character + ' ')
            file.write(str(self.occur_time) + ' ')
            for pos in self.pos_map:
                file.write(pos + ":" + str(self.pos_map[pos]) + ' ')
            file.write('\n')
        for child in self.children:
            self.children[child].save_node(former_letters + self.character, file)

    def __str__(self):
        rst_str = '字符：' + str(self.character)
        rst_str += '\t是否出现：' + str(self.terminal_flag)
        if self.terminal_flag:
            rst_str += '\t出现次数：' + str(self.occur_time)
            rst_str += '\n词性信息：'
            for pos in self.pos_map:
                rst_str += '\n词性：' + pos
                rst_str += '\t出现次数：' + str(self.pos_map[pos])
        return rst_str


class TrieTree:
    def __init__(self, pre_process_flag=True):
        self.root = {}
        self.max_len = 0
        self.pre_process_flag = pre_process_flag

    def add_word(self, word, part_of_speech):
        if len(word) > self.max_len:
            self.max_len = len(word)
        if self.pre_process_flag:
            word = pre_process(word)
        else:
            word = turn_zero(word)
        child = self.get_child_with(word[0])
        if child is None:
            child = TrieNode(word, part_of_speech)
            self.root[word[0]] = child
        else:
            child.add_child(word, part_of_speech)

    def get_child_with(self, character):
        if character not in self.root:
            return None
        return self.root[character]

    def get_child(self, word):
        if self.pre_process_flag:
            word = pre_process(word)
        else:
            word = turn_zero(word)
        i = 0
        child = self.get_child_with(word[0])
        if child is None:
            return None
        while i != len(word) - 1:
            i += 1
            child = child.get_child_with(word[i])
            if child is None:
                return None
        return child

    def get_word_info(self, word):
        if self.pre_process_flag:
            word = pre_process(word)
        else:
            word = turn_zero(word)
        child = self.get_child(word)
        if child is not None and child.is_terminal():
            return child.occur_time, child.pos_map
        else:
            return 1, None

    def with_prefix(self, prefix) -> Tuple[bool, TrieNode]:
        prefix = turn_zero(prefix)
        i = 0
        child = self.get_child_with(prefix[0])
        if child is None:
            return False, None
        while i != len(prefix) - 1:
            i += 1
            child = child.get_child_with(prefix[i])
            if child is None:
                return False, None
        return True, child

    def have_word(self, word):
        if self.pre_process_flag:
            word = pre_process(word)
        else:
            word = turn_zero(word)
        i = 0
        child = self.get_child_with(word[0])
        if child is None:
            return False
        while i != len(word) - 1:
            i += 1
            child = child.get_child_with(word[i])
            if child is None:
                return False
        return child.is_terminal()

    def save_trie(self, file: TextIO):
        file.write(str(self.max_len) + '\n')
        file.write(str(self.pre_process_flag) + '\n')
        for node in self.root:
            self.root[node].save_node("", file)
        file.write('END\n')

    def load_word(self, word, occur_time, pos_map):
        i = 0
        len_word = len(word)
        child = self.get_child_with(word[0])
        if child is None:
            temp_node = TrieNode('a', 'a')
            temp_node.occur_time = 0
            temp_node.pos_map = {}
            temp_children = self.root
            if len_word != 1:
                temp_node.terminal_flag = False
                temp_node.character = word[0]
                temp_children[word[0]] = temp_node
                i += 1
                while i != len_word:
                    temp_children = temp_node.children
                    temp_node = TrieNode('a', 'a')
                    temp_node.occur_time = 0
                    temp_node.pos_map = {}
                    if i == len_word - 1:
                        temp_node.character = word[0]
                        temp_node.occur_time = occur_time
                        temp_node.pos_map = pos_map
                    else:
                        temp_node.terminal_flag = False
                        temp_node.character = word[0]
                    temp_children[word[i]] = temp_node
                    i += 1
            else:
                temp_node.character = word[0]
                temp_node.occur_time = occur_time
                temp_node.pos_map = pos_map
                temp_children[word[0]] = temp_node
        else:
            i += 1
            while i != len_word:
                next_child = child.get_child_with(word[i])
                if next_child is None:
                    temp_node = child
                    while i != len_word:
                        temp_children = temp_node.children
                        temp_node = TrieNode('a', 'a')
                        temp_node.occur_time = 0
                        temp_node.pos_map = {}
                        if i == len_word - 1:
                            temp_node.character = word[0]
                            temp_node.occur_time = occur_time
                            temp_node.pos_map = pos_map
                        else:
                            temp_node.terminal_flag = False
                            temp_node.character = word[0]
                        temp_children[word[i]] = temp_node
                        i += 1
                else:
                    child = next_child
                    i += 1

    def load_trie(self, file: TextIO):
        line = file.readline().strip('\n')
        self.max_len = int(line)
        line = file.readline().strip('\n')
        self.pre_process_flag = bool(line)
        line = file.readline().strip('\n')
        while line != 'END':
            parts = line.split(' ')
            pos_map = {}
            for i in range(len(parts) - 3):
                pos, time = parts[i + 2].split(':')
                pos_map[pos] = int(time)
            self.load_word(parts[0], int(parts[1]), pos_map)
            line = file.readline().strip('\n')
