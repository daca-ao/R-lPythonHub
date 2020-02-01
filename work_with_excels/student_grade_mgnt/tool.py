# -*- coding: UTF-8 -*-

import pandas as pd
from const import *


def read_exam_for_class_excel(file_path):
    return pd.read_excel(file_path, names=EXAM_CLASS_COLUMN_NAME)
