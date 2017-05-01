# coding=gbk
import numpy as np
import pandas as pd
"""
    ���������ֵ�ת��Ϊ��Ӧ���ı�������ע��������ı�������ţ���Ҫͬʱ���������Ͷ�Ӧ���ֵ�
"""
def changeToFeatureVector(words,total_vova_value,target_file=None):
    """
    תΪ���������ע�����ĳЩѵ�����Ͳ��Լ��������NaN�����������0�����
    :param words: ��Ҫת��������
    :param total_vova_value: �ܵĴ���
    :param target_file:��Ҫд����ļ�Ŀ¼���ǰ�
    :return:
    """
    print("begin change to feature vector.")
    total_vova_value["sequence"] = list(range(1, len(total_vova_value) + 1))  #�������
    #���ִ�����ת��Ϊ����
    def f(x):
        return list(pd.Series(total_vova_value["sequence"][x]).fillna(0))  # ̫�����ˣ�DataFrame�����б����룬���Զ������б��ÿһ��Ԫ��
    words["sequence"] = words['content'].apply(f)  # ����ÿһ��words���ԣ���������������������Ȼ����ÿһ���ʣ�pn['words']�൱��ȡ����һ��series
    #��pnд���ļ���
    if target_file:
        words.to_csv(target_file,encoding="utf8")
    print("end change to feature vector.")

#��pd_data��content����תΪ��������������feature_name��һ���У�targetfile����ָ��Ҫ�������Ǹ��ļ�����ȥ
#�����vector�Ǻ����������Ĵ�Сһ��
def changeToBinaryVector(pd_data,voca_dict,target_file=None):
    print("voca_dict:",voca_dict)
    # ���ִ�����ת��Ϊ����
    def f(x):
        vector = []  # vector����ʵ��
        for word in voca_dict.index:
            if word in x:  #����������ĵ���
                vector.append(1)
            else:
                vector.append(0)  #�����NaN
        return vector
    pd_data["sequence"] = pd_data['content'].apply(f)  # ����ÿһ��words���ԣ���������������������Ȼ����ÿһ���ʣ�pn['words']�൱��ȡ����һ��series
    #��NaNת��0
    #pd_data['vector'] = pd_data['vector'].apply(lambda x:list(np.nan_to_num(x)))
    # ��pnд���ļ���
    if target_file:
        pd_data.to_csv(target_file,encoding="utf8")
