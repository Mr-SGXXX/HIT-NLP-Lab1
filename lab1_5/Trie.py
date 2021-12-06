from typing import Tuple
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
