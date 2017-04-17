# coding=gbk
import math
import types
"""
    ���ʵ�ת��Ϊ������������ʵ�����糣�õ���tf��word2vec�ȣ�������һ��bdc��df bdc
"""


def word2vec():

    pass


def getBDCVector(voca_dict,classnum,feature_name):
    """
    :param voca_dict: pandas dataframe
    :param classnum: ���ĸ��������������Ϊ2���������>2
    :param feature_name: ��Ҫ�������һ��
    :return: ����Ҫ���أ���Ϊ����
    """
    bdc_set = []
    # word_num[0]Ϊ���ʣ���ÿ���ʶ���
    for index, row in voca_dict.iterrows():
        posibility_list = []  #����ÿ�����еĸ���
        # ��ÿ���������
        for j in range(classnum):
            #__getOriginalValue��strתΪlist����������Ϊpandas���ļ��ж�ȡdataframeʱlist����str
            if row['class_word_appear_set'][j] == 0:
                posibility_list.append(0)
            else:
                posibility_list.append(float(row['word_appear_set'][j]) / float(row['class_word_appear_set'][j]))
        temp = 0
        for j in range(classnum):
            try:
                temp += (posibility_list[j] / sum(posibility_list)) * (
                math.log(posibility_list[j] / sum(posibility_list)))
            except:
                print("error:",posibility_list[j],sum(posibility_list))
                temp += 0
        temp /= math.log(classnum)
        bdc_set.append(1 + temp)
    print(bdc_set)
    voca_dict[feature_name] = bdc_set

#�����µ��뷨�е�df-bdcֵ����p(d,ci)��i�г��ִʵ��ĵ���ռ���ĵ�����
#���ݴʵ����DFBDCֵ��voca_dict�ĸ�ʽΪpandas dataframe�������ʱclassnum>2��������ʱclassnum=2����Ҫ��voca_dict��ʲô���ӵģ�
def getDFBDCVector(voca_dict,classnum,feature_name):
    df_bdc_set = []
    # word_num[0]Ϊ���ʣ���ÿ���ʶ���
    for index, row in voca_dict.iterrows():
        posibility_list = []  # ����ÿ�����еĸ���
        # ��ÿ���������
        for j in range(classnum):
            # __getOriginalValue��strתΪlist����������Ϊpandas���ļ��ж�ȡdataframeʱlist����str
            if row['doc_class_set'][j] == 0:
                posibility_list.append(0)
            else:
                posibility_list.append(float(row['word_doc_set'][j]) / float(row['doc_class_set'][j]))
        temp = 0
        for j in range(classnum):
            try:
                temp += (posibility_list[j] / sum(posibility_list)) * (
                    math.log(posibility_list[j] / sum(posibility_list)))
            except:
                print("error:", posibility_list[j], sum(posibility_list))
                temp += 0
        temp /= math.log(classnum)
        df_bdc_set.append(1 + temp)
    print(df_bdc_set)
    voca_dict[feature_name] = df_bdc_set
