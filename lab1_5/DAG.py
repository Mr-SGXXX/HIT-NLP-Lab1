from math import log
import numpy as np

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

    def HMM(self, pos_label_map, pos_num_map, state_trans_mat, total_word_num):
        # 后向算法
        sp = 0
        if pre_process(self.sentence[0:19]) == "\\linePosition":
            sp = 19
        s_len = len(self.sentence) - sp
        route = {s_len + sp: (0.0, 0, 1)}
        for start in range(s_len + sp - 1, sp - 1, -1):
            max_end = start
            max_state = 1
            max_log_beta = -float('inf')
            for end in self.dag[start]:
                for i in range(len(pos_label_map) - 2):
                    pos_times = pos_num_map[pos_label_map[i + 2]]
                    word_pos_map = self.dict_trie.get_word_info(self.sentence[start:end + 1])[1]
                    if word_pos_map is None or pos_label_map[i + 2] not in word_pos_map:
                        word_pos_times = pos_times / total_word_num
                    else:
                        word_pos_times = word_pos_map[pos_label_map[i + 2]]
                    if end == s_len + sp - 1:
                        temp_log = log(state_trans_mat[i + 2, 1]) - 2 * log(pos_times) \
                                   + log(word_pos_times)
                    else:
                        next_log, next_end, next_state = route[end + 1]
                        temp_log = next_log + log(state_trans_mat[i + 2, next_state]) \
                                   - 2 * log(pos_times) + log(word_pos_times)
                    if max_log_beta < temp_log:
                        max_log_beta = temp_log
                        max_state = i + 2
                        max_end = end
            route[start] = (max_log_beta, max_end, max_state)
        line = '' if sp == 0 else self.sentence[0:19] + '/ '
        i = sp
        while route[i][2] != 1:
            line += self.sentence[i:route[i][1] + 1] + '/ '
            i = route[i][1] + 1
        return line

    def max_frequency(self, total_word_num):
        s_len = len(self.sentence)
        route = {s_len: (0, 0)}
        log_total = log(total_word_num)
        for start in range(s_len - 1, -1, -1):
            max_end = start
            max_log = -float('inf')
            for end in self.dag[start]:
                log_v = log(self.dict_trie.get_word_info(self.sentence[start:end + 1])[0]) \
                        - log_total + route[end + 1][0]
                if log_v > max_log:
                    max_log = log_v
                    max_end = end
            route[start] = (max_log, max_end)
        line = ''
        i = 0
        while route[i][0] != 0:
            line += self.sentence[i:route[i][1] + 1] + '/ '
            i = route[i][1] + 1
        return line
