# coding=gbk
import pandas as pd
"""
    ���ݶ�ȡ��utils��
"""

def read_csv(source_file):
    source = pd.read_csv(source_file,index_col=0)
    print(source)
    return source