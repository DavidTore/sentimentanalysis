# coding=gbk
import utils.sentiment_data_path as sdp
import neuralnetwork.preprocess.data_clean.import_data as id
import neuralnetwork.preprocess.voca_dict.voca_data as vd
import neuralnetwork.preprocess.generate_vector.feature as feature
import neuralnetwork.preprocess.generate_vector.transfer_vector as tv
import pandas as pd
"""
    ����Ԥ�����Ӧ����ѵ���������Լ����ֵ䣬����ѵ�����Ͳ��Լ������������������ʹ��wordembedding
"""
def __voca_dict(class_num,pos_file,neg_file,voca_csv=None):
    """
    ����ѵ���������Լ��Լ��ʵ�
    :param class_num: һ���ж������
    :param pos_file:�����ļ�
    :param neg_file:�����ļ�
    :param voca_csv: �ʵ�·�������������д���ļ���
    :return: ����ѵ���������Լ����ʵ��Լ���Ӧ��wordembedding
    """

    pd_train, pd_test = id.getTrainAndTest(pos_file,neg_file)  #��ȡ���ݲ�תΪdataframe

    # pd_train = pd_train.head(1000)  #����ѵ��������
    # pd_test = pd_test.head(200)    #���Ʋ��Լ�����

    voca_dict = vd.getRelativeValue(pd_train, vd.getUniqueVocabulary(pd_train),
                                    class_num)  # getUniqueVocabulary�ȽϺ�ʱ���洢��csv��

    # �������Ӹ���term weighting schema�����������
    feature.getBDCVector(voca_dict, class_num, "bdc")  # �����ֵ����BDCֵ����Ҫָ��index
    feature.getDFBDCVector(voca_dict, class_num, "df_bdc")  # �����ֵ����DF_BDCֵ����Ҫָ��index

    if voca_csv:  # ���������д���ļ���
        voca_dict.to_csv(voca_csv)

    print(voca_dict)
    return pd_train, pd_test, voca_dict

def __generate_vector(pd_train,pd_test,voca_dict,feature_name,train_csv=None,test_csv=None):
    """
    ת���ɲ�ͬ������
    :param pd_train:ѵ������dataframe����
    :param pd_test:���Լ���dataframe����
    :param voca_dict:�ʵ䣬��¼��һЩ����
    :param feature_name:��Ҫת��������
    :param embedding_dim: wordembedding��ά��
    :param embedding_csv: wordembedding��ά��
    :param train_csv:��Ҫ�洢��ѵ�����ļ�
    :param test_csv:��Ҫ�洢�Ĳ��Լ��ļ�
    :return:�޷��أ����Ǵ���
    """
    pd_train_copy = pd_train.copy()  #��ֹ���ݸ���
    pd_test_copy = pd_test.copy()

    # ���Լ���ѵ����תΪ����������������ʹ�������
    tv.changeToFeatureVector(pd_train_copy, voca_dict, feature_name)
    tv.changeToFeatureVector(pd_test_copy, voca_dict, feature_name)
    if train_csv:
        pd_train_copy.to_csv(train_csv,encoding="utf8")  # д��ѵ���ļ���
    if test_csv:
        pd_test_copy.to_csv(test_csv,encoding="utf8")  # д������ļ���

if __name__ == '__main__':
    feature_name = "tf"
    #����ֻ���ֻ��������������ֻ��������
    pd_train, pd_test, voca_dict = __voca_dict(2, sdp.POS_COMMENT, sdp.NEG_COMMENT, voca_csv=sdp.VOCA_COMMENT)

    #ת�����������
    __generate_vector(pd_train, pd_test, voca_dict,feature_name,train_csv=sdp.TRAIN_COMMENT, test_csv=sdp.TEST_COMMENT)


