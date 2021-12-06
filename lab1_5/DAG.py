import math

from Trie import TrieTree
from utils import pre_process


class DAG:
    def __init__(self, sentence, dict_trie: TrieTree, prefix_trie):
        self.dag = {}
        self.sentence = sentence
        self.dict_trie = dict_trie
        s_len = len(sentence)
        for k in range(s_len):
            tmp_list = []
            i = k
            tmp = sentence[k]
            prefix_flag, prefix_node = prefix_trie.with_prefix(tmp)
            while i < s_len and prefix_flag:
                if prefix_node.is_terminal():
                    tmp_list.append(i)
                i += 1
                tmp = sentence[k:i + 1]
                prefix_flag, prefix_node = prefix_trie.with_prefix(tmp)  # 前缀树里没有不存在的段落号单词，导致图里没有这个单词
            if not tmp_list:
                tmp_list.append(k)
            self.dag[k] = tmp_list

    def HMM(self, pos_label_map, pos_num_map, state_trans_mat):
        s_len = len(self.sentence)
        route = {s_len: (0, 0)}
        next_pos = 'ed'
        for start in range(s_len - 1, -1, -1):
            max_end = 0
            max_log = -float('inf')
            for end in self.dag[0]:
                log = 1
                if log > max_log:
                    max_log = log
                    max_end = end

            if pre_process(self.sentence[0:max_end]) == "\\linePosition":
                pass

    def max_frequency(self, total_word_num):
        s_len = len(self.sentence)
        route = {s_len: (0, 0)}
        log_total = math.log(total_word_num)
        for start in range(s_len - 1, -1, -1):
            max_end = start
            max_log = -float('inf')
            for end in self.dag[start]:
                log = math.log(self.dict_trie.get_word_info(self.sentence[start:end + 1])[0]) \
                      - log_total + route[end + 1][0]
                if log > max_log:
                    max_log = log
                    max_end = end
            route[start] = (max_log, max_end)
        line = ''
        i = 0
        while route[i][0] != 0:
            line += self.sentence[i:route[i][1] + 1] + '/ '
            i = route[i][1] + 1
        return line
