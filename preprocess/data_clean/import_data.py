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
    pd_data = pd.read_csv(filename)
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
    pass


if __name__ == '__main__':
    import_comment()



