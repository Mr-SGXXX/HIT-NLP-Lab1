# 实验一第五部分 - 基于统计语言模型的分词系统实现
from load_data import load_dict
from DAG import DAG

if __name__ == "__main__":
    Dict_trie, Pos_label_Map, Pos_num_map, \
    Total_word_num, State_trans_mat = load_dict(-1, 10, ["../res/199801_seg&pos.txt"])
    dag = DAG("迈向充满希望的新世纪——一九九八年新年讲话（附图片１张）", Dict_trie)
    print("a")
