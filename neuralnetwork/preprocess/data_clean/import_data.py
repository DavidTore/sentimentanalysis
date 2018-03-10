# coding=gbk
import utils.sentiment_data_path as sdp
import utils.read_data as rd
import pandas as pd
import utils.change_data as change
"""
    ���ݵ��룬��ȡ��ѵ�����Ͳ��Լ�
"""
def getTrainAndTest(pos_file,neg_file):
    """
    ÿ�����г�ȡ20%��Ϊ���Լ���ע������������ԣ���Ϊ��ȡ�����Ѿ��ֺôʵ��ļ���������Ҫ��eval����ת��
    :param pos_file:
    :param neg_file:
    :return:
    """
    pd_pos_data = rd.read_csv(pos_file) #��ȡ�������ݲ�תΪpandas dataframe
    pd_neg_data = rd.read_csv(neg_file)

    pd_train = pd_pos_data.head(int(len(pd_pos_data)*0.8)).append(pd_neg_data.head(int(len(pd_neg_data)*0.8)),ignore_index=True)  #ѵ����ռ80%
    pd_test = pd_pos_data.tail(len(pd_pos_data) - int(len(pd_pos_data)*0.8)).append(pd_neg_data.tail(len(pd_neg_data) - int(len(pd_neg_data)*0.8)), ignore_index=True)  # ���Լ�ռ20%

    pd_train['content'] = pd_train['content'].apply(change.getOriginalValue)
    pd_train['class'] = pd_train['class'].apply(change.getOriginalValue)
    pd_test['content'] = pd_test['content'].apply(change.getOriginalValue)
    pd_test['class'] = pd_test['class'].apply(change.getOriginalValue)

    print(pd_train)
    print(pd_test)
    print(pd_train['description'],pd_train["content"])
    return (pd_train,pd_test)

if __name__ == '__main__':
    pos_file = sdp.POS_COMMENT
    neg_file = sdp.NEG_COMMENT
    getTrainAndTest(pos_file, neg_file)
