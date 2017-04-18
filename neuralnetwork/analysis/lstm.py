# coding=gbk
import pandas as pd
import numpy as np
import utils.sentiment_data_path as sdp
import utils.read_data as rd
import utils.change_data as cd
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras.layers.core import Dropout,Dense,Activation
from keras.utils import np_utils  #���ʹ�û����Ǻ����

"""
    ͨ��kerasʵ��lstm�����磬ʵ����ֻҪȷ���ñ�ǩ�����롢�ֵ䣬�Ϳ���ѵ����������
"""
def embedding_matrix(vova_csv,embedding_dim,feature_name):
    """
    ����embedding_matrix
    :param vova_value: �ʵ�
    :param embedding_dim: ÿ��������ά�ȣ�����tf��bdc�ȶ���1
    :return:
    """
    #��vova_csv�ж�ȡ�ļ�
    vova_value = rd.read_csv(vova_csv,encoding="gbk")
    print(vova_value)
    embedding_matrix = np.zeros((len(vova_value) + 1, embedding_dim))
    vova_value_list = list(vova_value[feature_name])
    for i in range(len(vova_value)):
        embedding_matrix[i+1] = np.array([vova_value_list[i]])
    return embedding_matrix


def lstm(trainData,trainMark,testData,testMark,embedding_dim,embedding_matrix,maxlen):
    # ������ݣ���ÿ�����г��ȱ���һ��
    trainData = list(sequence.pad_sequences(trainData,maxlen=maxlen,dtype='float64'))  # sequence���ص���һ��numpy���飬pad_sequences�������ָ�����ȵ����У�����׶Σ�����0�������������Ϊ0ʱ����ӦֵҲΪ0����˿�������
    testData = list(sequence.pad_sequences(testData,maxlen=maxlen,dtype='float64'))  # sequence���ص���һ��numpy���飬pad_sequences�������ָ�����ȵ����У�����׶Σ�����0

    # ����lstm������ģ��
    model = Sequential()  # ������������Զѵ�������ͨ������һ��layer��list�������ģ�ͣ�Ҳ����ͨ��.add()����һ�����ļ��ϲ�
    #model.add(Dense(256, input_shape=(train_total_vova_len,)))   #ʹ��ȫ���ӵ������
    model.add(Embedding(len(embedding_matrix),embedding_dim,weights=[embedding_matrix],mask_zero=True,input_length=maxlen))  # ָ������㣬����ά��one-hotת�ɵ�ά��embedding��ʾ����һ������������0��������������������±�+1���ڶ�����������0������������ȫ����Ƕ���ά��
    # lstm�㣬Ҳ�ǱȽϺ��ĵĲ�
    model.add(LSTM(128))  # 256��ӦEmbedding���ά�ȣ�128������ά�ȿ����Ƶ�����
    model.add(Dropout(0.5))  # ÿ���ڲ������µ�ʱ����һ���ļ��ʶϿ�������ӣ����ڷ�ֹ�����
    model.add(Dense(1))  # ȫ���ӣ�������������㣬1���������ά�ȣ�128����LSTM��ά�ȿ��������Ƶ�����
    model.add(Activation('sigmoid'))  # �����sigmoid�����
    # �����ģ�ͣ�binary_crossentropy�������������ʧ��logloss����adam��һ���Ż�����class_mode��ʾ����ģʽ
    model.compile(loss='binary_crossentropy', optimizer='adam', class_mode="binary")

    # ��ʽ���и�ģ��,��֪��Ϊʲô�ˣ���Ϊû�в�0����ÿ��array�ĳ����ǲ�һ���ģ���˲Żᱨ��
    X = np.array(list(trainData))  # ��������
    print("X:", X)
    Y = np.array(list(trainMark))  # ��ǩ
    print("Y:", Y)
    # batch_size��������ָ�������ݶ��½�ʱÿ��batch������������
    # nb_epoch��������ѵ����������ѵ�����ݽ��ᱻ����nb_epoch��
    model.fit(X, Y, batch_size=16, nb_epoch=10)  # �ú�����X��YӦ���Ƕ�����룺numpy list(����ÿ��Ԫ��Ϊnumpy.array)���������룺numpy.array

    # ����Ԥ��
    A = np.array(list(testData))  # ��������
    print("A:", A)
    B = np.array(list(testMark))  # ��ǩ
    print("B:", B)
    classes = model.predict_classes(A)  # �����Ԥ�������
    acc = np_utils.accuracy(classes, B)  # ����׼ȷ�ʣ�ʹ�û����Ǻ����
    print('Test accuracy:', acc)

if __name__ == '__main__':
    vova_csv = sdp.VOCA_COMMENT
    embedding_dim = 1
    maxlen = 50
    feature_name = "df_bdc"
    #���embedding����
    embedding_matrix = embedding_matrix(vova_csv, embedding_dim, feature_name)

    #���ѵ�����ݺͲ�������
    pd_train = rd.read_csv(sdp.TRAIN_COMMENT,encoding="utf8")
    pd_test = rd.read_csv(sdp.TEST_COMMENT,encoding="utf8")

    def f(x):
        if eval(x) == [1,0]:
            return 1
        else:
            return 0
    pd_train['sequence'] = pd_train['sequence'].apply(cd.getOriginalValue)  #�������
    pd_test['sequence'] = pd_test['sequence'].apply(cd.getOriginalValue)

    pd_train['class'] = pd_train['class'].apply(f)
    pd_test['class'] = pd_test['class'].apply(f)

    lstm(list(pd_train['sequence']), list(pd_train['class']), list(pd_test['sequence']), list(pd_test['class']), embedding_dim,embedding_matrix,maxlen)