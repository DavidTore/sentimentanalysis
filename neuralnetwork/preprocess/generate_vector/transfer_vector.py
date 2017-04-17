# coding=gbk
import numpy as np
import pandas as pd
"""
    ���������ֵ�ת��Ϊ��Ӧ���ı�������ע��������ı�������ţ���Ҫͬʱ���������Ͷ�Ӧ���ֵ�
"""
#תΪ���������ע�����ĳЩѵ�����Ͳ��Լ��������NaN�����������0�����
def changeToFeatureVector(words,total_vova_value,name,target_file=None):
    total_vova_value[name] = list(range(1, len(total_vova_value) + 1))
    #���ִ�����ת��Ϊ����
    def f(x,name):
        #print("name:",name)
        return list(pd.Series(total_vova_value[name][x]).fillna(0))  # ̫�����ˣ�DataFrame�����б����룬���Զ������б��ÿһ��Ԫ��
    words[name] = words['content'].apply((lambda x:f(x,name)))  # ����ÿһ��words���ԣ���������������������Ȼ����ÿһ���ʣ�pn['words']�൱��ȡ����һ��series
    #��pnд���ļ���
    if target_file:
        words.to_excel(target_file)