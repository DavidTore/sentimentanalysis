# coding=gbk
import pandas as pd
import jieba as jb
import utils.sentiment_data_path as sdata
import utils.sentiment_dict_path as sdict

"""
    ���ݵ��룬��txt��csv��excel�ȣ�ͬ��ת����pandas dataframe���ֺôʲ��洢��csv��
"""
#��pandas��ȡcsv���ݲ�ת�����б��ʽ��ע��ִʺ�����ݶ�������content��
def __read_data(filename):
    pd_data = pd.read_csv(filename,index_col=0)
    #��pd_data��ÿһ�����ݽ��л�ԭ
    # for name in pd_data.index:
    #     pd_data[name] = pd_data[name].apply(lambda x:eval(x))
    return pd_data

def import_comment():
    pos_comment = __read_data(sdata.POS_COMMENT)
    neg_comment = __read_data(sdata.NEG_COMMENT)
    print(pos_comment)
    print(neg_comment)
    #���ػ�������������
    return (pos_comment,neg_comment)

def import_weibo():
    pos_weibo = __read_data(sdata.POS_WEIBO)
    neg_weibo = __read_data(sdata.NEG_WEIBO)
    print(pos_weibo)
    print(neg_weibo)
    # ���ػ�������������
    return (pos_weibo, neg_weibo)

def import_sentiment_dict():
    pos = __read_data(sdict.POS_DICT)
    neg = __read_data(sdict.NEG_DICT)
    plus = __read_data(sdict.PLUS_DICT)
    no = __read_data(sdict.NO_DICT)
    print(pos)
    print(neg)
    print(plus)
    print(no)
    # ���ػ�������������
    return (pos,neg,plus,no)


if __name__ == '__main__':
    #import_comment()   #pos:10676��  neg:10427
    #import_weibo()    #pos:199574  neg:51743  #���������е���Ӧ�ð��������ָ���ļӽ�ȥ
    import_sentiment_dict()  #pos:6506  neg:11185  plus:182  no:18

    pass



