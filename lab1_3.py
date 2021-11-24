# 实验一第三部分 - 正反向最大匹配分词效果分析

SEG_STD_PATH = "./res/199801_seg&pos.txt"
SEG_FMM_PATH = "./res/seg_FMM.txt"
SEG_BMM_PATH = "./res/seg_BMM.txt"
SCORE_PATH = "./res/score.txt"

Correct_num_FMM = 0
Total_num_FMM = 0
Correct_num_BMM = 0
Total_num_BMM = 0
Total_num_STD = 0


def compare_by_line(line_STD, line_FMM, line_BMM):
    global Correct_num_FMM, Total_num_FMM, Correct_num_BMM, Total_num_BMM, Total_num_STD
    start_pos_STD = 0
    cur_pos_STD = 0
    len_STD = len(line_STD)
    start_pos_FMM = 0
    cur_pos_FMM = 0
    len_FMM = len(line_FMM)
    start_pos_BMM = 0
    cur_pos_BMM = 0
    len_BMM = len(line_BMM)
    if len_STD == 1:
        return
    while cur_pos_STD != len_STD or cur_pos_FMM != len_FMM or cur_pos_BMM != len_BMM:
        if line_STD[cur_pos_STD] != line_FMM[cur_pos_FMM] or line_STD[cur_pos_STD] != line_BMM[cur_pos_BMM]:
            print("代码有问题：字符没对齐")
            raise ValueError
        if line_STD[start_pos_STD: cur_pos_STD] == line_FMM[start_pos_FMM: cur_pos_FMM] and \
                line_FMM[cur_pos_FMM + 1] == line_STD[cur_pos_STD + 1] and \
                line_STD[cur_pos_STD + 1] == '/':
            Correct_num_FMM += 1
        if line_STD[start_pos_STD: cur_pos_STD] == line_BMM[start_pos_BMM: cur_pos_BMM] and \
                line_BMM[cur_pos_BMM + 1] == line_STD[cur_pos_STD + 1] and \
                line_STD[cur_pos_STD + 1] == '/':
            Correct_num_BMM += 1
        cur_pos_STD += 1
        cur_pos_FMM += 1
        cur_pos_BMM += 1
        if line_STD[cur_pos_STD] == '/':
            while line_STD[cur_pos_STD] != ' ' and cur_pos_STD < len_STD:
                cur_pos_STD += 1
            Total_num_STD += 1
            cur_pos_STD += 1
            if cur_pos_STD < len_STD and line_STD[cur_pos_STD] == '[':
                cur_pos_STD += 1
            start_pos_STD = cur_pos_STD
        if line_FMM[cur_pos_FMM] == '/':
            Total_num_FMM += 1
            cur_pos_FMM += 2
            start_pos_FMM = cur_pos_FMM
        if line_BMM[cur_pos_BMM] == '/':
            Total_num_BMM += 1
            cur_pos_BMM += 2
            start_pos_BMM = cur_pos_BMM



def save_rst():
    global Correct_num_FMM, Total_num_FMM, Correct_num_BMM, Total_num_BMM, Total_num_STD
    score_file = open(SCORE_PATH, 'w')
    P_FMM = Correct_num_FMM / Total_num_FMM
    P_BMM = Correct_num_BMM / Total_num_BMM
    R_FMM = Correct_num_FMM / Total_num_STD
    R_BMM = Correct_num_BMM / Total_num_STD
    F_FMM = 2 * P_FMM * R_FMM / (P_FMM + R_FMM)
    F_BMM = 2 * P_BMM * R_BMM / (P_BMM + R_BMM)
    score_file.write("FMM:\n Precision:" + str(P_FMM) + "\tRecall:" + str(R_FMM) + "\tF-measure:" + str(F_FMM) + '\n')
    score_file.write("BMM:\n Precision:" + str(P_BMM) + "\tRecall:" + str(R_BMM) + "\tF-measure:" + str(F_BMM) + '\n')
    score_file.close()


if __name__ == "__main__":
    Seg_STD_file = open(SEG_STD_PATH, 'r')
    Seg_FMM_file = open(SEG_FMM_PATH, 'r')
    Seg_BMM_file = open(SEG_BMM_PATH, 'r')
    Line_STD = Seg_STD_file.readline()
    Line_FMM = Seg_FMM_file.readline()
    Line_BMM = Seg_BMM_file.readline()
    while Line_STD != '':
        compare_by_line(' '.join(Line_STD.split()) + ' ', ' '.join(Line_FMM.split()) + ' ',
                        ' '.join(Line_BMM.split()) + ' ')
        Line_STD = Seg_STD_file.readline()
        Line_FMM = Seg_FMM_file.readline()
        Line_BMM = Seg_BMM_file.readline()
    save_rst()
    Seg_STD_file.close()
    Seg_FMM_file.close()
    Seg_BMM_file.close()
