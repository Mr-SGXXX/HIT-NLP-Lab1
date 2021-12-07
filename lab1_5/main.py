# 实验一第五部分 - 基于统计语言模型000000000000的分词系统实现
from load_data import load_test, load_dict
from DAG import DAG
from cal_rst import cal_rst

SEG_DATA_PATH1 = "../res/199801_seg&pos.txt"
SEG_DATA_PATH2 = "../res/199802.txt"
RAW_DATA_PATH = "../res/199801_sent.txt"
SCORE_PATH = "./output/score.txt"
SEG_PATH = "./output/seg.txt"

N_GRAM = True

if __name__ == "__main__":
    Dict_trie, Prefix_trie, Pos_label_Map, Pos_num_map, \
    Total_word_num, State_trans_mat = load_dict(0, 10, [SEG_DATA_PATH1, SEG_DATA_PATH2], [1])
    Raw_lines, True_lines = load_test(0, 10, RAW_DATA_PATH, SEG_DATA_PATH1)
    Cal_lines = []
    for line in Raw_lines:
        dag = DAG(line, Dict_trie, Prefix_trie)
        if N_GRAM:
            Cal_lines.append(dag.HMM(Pos_label_Map, Pos_num_map, State_trans_mat))
        else:
            Cal_lines.append(dag.max_frequency(Total_word_num))
    cal_rst(Cal_lines, True_lines, SCORE_PATH, SEG_PATH)
    print("a")
