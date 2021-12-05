Correct_num = 0
Total_num = 0
Total_num_STD = 0


def cal_rst(cal_lines, true_lines, score_path, seg_path):
    global Correct_num, Total_num, Total_num_STD
    with open(seg_path, 'w') as seg_file:
        for i in range(len(cal_lines)):
            line_STD = true_lines[i]
            line = cal_lines[i]
            seg_file.write(line + '\n')
            compare_by_line(' '.join(line_STD.split()) + ' ', ' '.join(line.split()) + ' ')
    P = Correct_num / Total_num
    R = Correct_num / Total_num_STD
    F = 2 * P * R / (P + R)
    with open(score_path, 'a') as score_file:
        score_file.write("Precision:" + str(P) + "\tRecall:" + str(R) + "\tF-measure:" + str(F) + '\n')


def compare_by_line(line_STD, line):
    global Correct_num, Total_num, Total_num_STD
    start_pos_STD = 0
    cur_pos_STD = 0
    len_STD = len(line_STD)
    start_pos = 0
    cur_pos = 0
    len_cal = len(line)
    if len_STD == 1:
        return
    while cur_pos_STD != len_STD or cur_pos != len_cal:
        if line_STD[cur_pos_STD] != line[cur_pos]:
            print("代码有问题：字符没对齐")
            raise ValueError
        if line_STD[start_pos_STD: cur_pos_STD] == line[start_pos: cur_pos] and \
                line[cur_pos + 1] == line_STD[cur_pos_STD + 1] and \
                line_STD[cur_pos_STD + 1] == '/':
            Correct_num += 1
        cur_pos_STD += 1
        cur_pos += 1
        if line_STD[cur_pos_STD] == '/':
            while line_STD[cur_pos_STD] != ' ' and cur_pos_STD < len_STD:
                cur_pos_STD += 1
            Total_num_STD += 1
            cur_pos_STD += 1
            if cur_pos_STD < len_STD and line_STD[cur_pos_STD] == '[':
                cur_pos_STD += 1
            start_pos_STD = cur_pos_STD
        if line[cur_pos] == '/':
            Total_num += 1
            cur_pos += 2
            start_pos = cur_pos
