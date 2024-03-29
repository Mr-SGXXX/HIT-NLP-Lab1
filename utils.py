def pre_process(word):
    if is_num(word):
        word = "\\number"
    elif is_num(word[:-1]) and word[-1] == '年' and 5 >= len(word) > 2 and\
            '十' not in word and '百' not in word and '千' not in word:
        word = "\\timeYear"
    elif is_num(word[:-1]) and word[-1] == '月' and (len(word) == 3 or len(word) == 2):
        word = "\\timeMonth"
    elif is_num(word[:-1]) and word[-1] == '日' and (len(word) == 3 or len(word) == 2):
        word = "\\timeDay"
    elif is_num(word[:-1]) and word[-1] == '．':
        word = "\\seqNum"
    elif is_num(word[:-1]) and word[-1] == '％' or word[0:3] == "百分之" and is_num(word[3:]):
        word = "\\percent"
    elif is_num(word[1:]) and word[0] == '第':
        word = "\\nth"

    position_parts = word.split('-')
    if len(position_parts) == 4 and is_num(position_parts[0]) and \
            is_num(position_parts[1]) and is_num(position_parts[2]) and \
            is_num(position_parts[3]) and len(position_parts[3]) == 3:
        word = "\\linePosition"

    ratio_parts = word.split('∶')
    if len(ratio_parts) != 1:
        if is_num(ratio_parts[0]) and is_num(ratio_parts[1]):
            word = "\\ratio"
    return word


def is_num(word):
    word = word.replace("○", "零")
    word = word.replace("点", "．")
    if len(word) > 1 and word[0] == '－':
        word = word[1:]
    dig_flag = False
    not_dig = False
    for c in word:
        if not dig_flag and c.isdigit():
            dig_flag = True
        if not not_dig and c.isnumeric() and not c.isdigit():
            not_dig = True
        if dig_flag and not_dig:
            return False
    if word.isnumeric():
        return True
    float_parts = word.split('．')
    if len(float_parts) != 1:
        if float_parts[0].isnumeric() and float_parts[1].isnumeric():
            return True
    float_parts = word.split('·')
    if len(float_parts) != 1:
        if float_parts[0].isnumeric() and float_parts[1].isnumeric():
            return True
    return False
