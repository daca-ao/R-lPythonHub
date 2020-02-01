# -*- coding: UTF-8 -*-

import configparser
import pandas as pd
import matplotlib.pyplot as plt
from const import *
from tool import *

# COLS
student_num_col = 'Num'
student_name_col = 'Name'
class_name_col = 'Class'
major_name_col = 'Maj'
minor_1_name_col = 'M1'
minor_2_name_col = 'M2'
chinese_rank_col = 'Ch-Rank'
math_rank_col = 'M-Rank'
english_rank_col = 'En-Rank'
major_rank_col = 'Maj-Rank'
minor_1_rank_col = 'M1-Rank'
minor_2_rank_col = 'M2-Rank'
four_rank_col = '4-Rank'
total_rank_col = 'Rank'
info_cols = [
    student_num_col,
    student_name_col,
    chinese_rank_col,
    math_rank_col,
    english_rank_col,
    major_rank_col,
    minor_1_rank_col,
    minor_2_rank_col,
    four_rank_col,
    total_rank_col
]


# read configs & exam data sheets
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
exams = []
for path in config[GROUP_PATH_FOR_CLASS]:
    exam_records_path = config[GROUP_PATH_FOR_CLASS][path]
    exams.append(read_exam_for_class_excel(exam_records_path))

class_name = exams[0][class_name_col][0]
exams_num = len(exams)
for exam in exams:
    assert class_name == exam[class_name_col][0]
print("已录入%s共%d次考试的成绩" % (class_name, exams_num))


info_dic = {}
infos = []
for i, exam in enumerate(exams):
    for col in info_cols[2:]:
        info_dic[col] = COLUMN_FORMAT % (col, i)
    infos.append(exam[info_cols].rename(columns=info_dic))

result = infos[0]
for info in infos[1:]:
    result = pd.merge(result, info, how='outer', on=[
                      student_num_col, student_name_col])

# add diff cols
for index in range(exams_num-1):
    result["Ch-Rank-Diff-%d" % (index+1)] = result[COLUMN_FORMAT %
                                                   (chinese_rank_col, index+1)]-result[COLUMN_FORMAT % (chinese_rank_col, index)]
    result["M-Rank-Diff-%d" % (index+1)] = result[COLUMN_FORMAT %
                                                  (math_rank_col, index+1)]-result[COLUMN_FORMAT % (math_rank_col, index)]
    result["En-Rank-Diff-%d" % (index+1)] = result[COLUMN_FORMAT %
                                                   (english_rank_col, index+1)]-result[COLUMN_FORMAT % (english_rank_col, index)]
    result["Maj-Rank-Diff-%d" % (index+1)] = result[COLUMN_FORMAT %
                                                    (major_rank_col, index+1)]-result[COLUMN_FORMAT % (major_rank_col, index)]
    result["M1-Rank-Diff-%d" % (index+1)] = result[COLUMN_FORMAT %
                                                   (minor_1_rank_col, index+1)]-result[COLUMN_FORMAT % (minor_1_rank_col, index)]
    result["M2-Rank-Diff-%d" % (index+1)] = result[COLUMN_FORMAT %
                                                   (minor_2_rank_col, index+1)]-result[COLUMN_FORMAT % (minor_2_rank_col, index)]
    result["4-Rank-Diff-%d" % (index+1)] = result[COLUMN_FORMAT %
                                                  (four_rank_col, index+1)]-result[COLUMN_FORMAT % (four_rank_col, index)]
    result["Rank-Diff-%d" % (index+1)] = result[COLUMN_FORMAT %
                                                (total_rank_col, index+1)]-result[COLUMN_FORMAT % (total_rank_col, index)]

# output query results
output_dic = {
    '语文': 'Ch-Rank-Diff-',
    '数学': 'M-Rank-Diff-',
    '英语': 'En-Rank-Diff-',
    exams[0][major_name_col][0]: 'Maj-Rank-Diff-',
    exams[0][minor_1_name_col][0]: 'M1-Rank-Diff-',
    exams[0][minor_2_name_col][0]: 'M2-Rank-Diff-',
    '4科': '4-Rank-Diff-',
    '总分': 'Rank-Diff-'
}
# output students whose marks in continious decreament
for key in output_dic:
    cols = [column for column in result.columns if column.startswith(
        output_dic[key])]
    decrease = result[-(result[cols] > 0).any(1)]
    decrease.set_index([student_num_col, student_name_col], inplace=True)
    print("%s持续退步的同学：\n" % key, decrease[cols])

# TODO print line charts
