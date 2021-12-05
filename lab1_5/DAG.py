from Trie import TrieTree
from utils import pre_process

class DAG:
    def __init__(self, sentence, dict_trie: TrieTree):
        self.dag = {}
        self.dict_trie = dict_trie
        s_len = len(sentence)
        for k in range(s_len):
            tmp_list = []
            i = k
            tmp = sentence[k]
            prefix_flag, prefix_node = dict_trie.with_prefix(tmp)
            while i < s_len and prefix_flag:
                if prefix_node.is_terminal():
                    tmp_list.append(i)
                i += 1
                tmp = pre_process(sentence[k:i + 1])
                prefix_flag, prefix_node = dict_trie.with_prefix(tmp)
            if not tmp_list:
                tmp_list.append(k)
            self.dag[k] = tmp_list

    def HMM(self, pos_label_map, pos_num_map, state_trans_mat):
        pass

    def max_frequency(self, total_word_num):
        pass
