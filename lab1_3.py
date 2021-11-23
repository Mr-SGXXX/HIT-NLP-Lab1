# 实验一第三部分 - 正反向最大匹配分词效果分析

SEG_STD_PATH = "./res/199801_seg&pos.txt"
SEG_FMM_PATH = "./res/seg_FMM.txt"
SEG_BMM_PATH = "./res/seg_BMM.txt"
SCORE_PATH = "/res/score.txt"

Correct_num_FMM = 0
Total_num_FMM = 0
Correct_num_BMM = 0
Total_num_BMM = 0
Total_num_STD = 0


def compare_by_line(line_STD, line_FMM, line_BMM):
    global Correct_num_FMM, Total_num_FMM, Correct_num_BMM, Total_num_BMM, Total_num_STD



def save_rst():
    global Correct_num_FMM, Total_num_FMM, Correct_num_BMM, Total_num_BMM, Total_num_STD
    score_file = open(SCORE_PATH, 'r')
    P_FMM = Correct_num_FMM / Total_num_FMM
    P_BMM = Correct_num_BMM / Total_num_BMM
    R_FMM = Correct_num_FMM / Total_num_STD
    R_BMM = Correct_num_BMM / Total_num_STD
    F_FMM = 2 * P_FMM * R_FMM / (P_FMM + R_FMM)
    F_BMM = 2 * P_BMM * R_BMM / (P_BMM + R_BMM)
    score_file.write("FMM:\n Precision:" + str(P_FMM) + "Recall:" + str(R_FMM) + "F-measure:" + str(F_FMM) + '\n')
    score_file.write("BMM:\n Precision:" + str(P_BMM) + "Recall:" + str(R_BMM) + "F-measure:" + str(F_BMM) + '\n')
    score_file.close()


if __name__ == "__main__":
    Seg_STD_file = open(SEG_STD_PATH, 'r')
    Seg_FMM_file = open(SEG_FMM_PATH, 'r')
    Seg_BMM_file = open(SEG_BMM_PATH, 'r')
    Line_STD = Seg_STD_file.readline()
    Line_FMM = Seg_FMM_file.readline()
    Line_BMM = Seg_BMM_file.readline()
    while Line_STD != '':
        compare_by_line(Line_STD, Line_FMM, Line_BMM)
        Line_STD = Seg_STD_file.readline()
        Line_FMM = Seg_FMM_file.readline()
        Line_BMM = Seg_BMM_file.readline()
    save_rst()
    Seg_STD_file.close()
    Seg_FMM_file.close()
    Seg_BMM_file.close()
