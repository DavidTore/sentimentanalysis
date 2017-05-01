# coding=gbk
"""
    knn�����ĵ���
"""
import time
import numpy as np
import pandas as pd
import machinelearning.analysis.knn.knn_sklearn as knn
import utils.sentiment_data_path as sdp


#Ĭ�ϲ���
K_LIST = 50
FLOD_NUM = 5  #���۽���ʵ��
CONFIRM_POS_CLASS = 0  #ָ���������������

#��ö��������ݣ�ֻ��Ҫ�Ķ�class�о���
def get_binary_class_data(train_csv,test_csv,voca_csv,feature_name):
    # ���ݶ�ȡ�����ȶ�ȡ�����������һ��comment����
    print("begin reading")
    pd_train = pd.read_csv(train_csv,index_col=0)  #���Ϊ0�Ļ�������0���Ǳ��1��ʼ
    pd_test = pd.read_csv(test_csv,index_col=0)

    #����������
    pd_train = pd_train.head(100)
    pd_test = pd_test.head(20)

    # ��ȡ�ֵ�
    voca_dict = pd.read_csv(voca_csv,index_col=0)

    print("end reading.")

    # def f(x):
    #     x = (pd.Series(eval(x))-1).replace(-1,np.nan)  #����תΪseries���У���Ҫ��ȥ1
    #     voca_index =  list(pd.Series(voca_dict.index)[x])  #����nan�򲻽��в�����������ҪתΪlist����������reindex�Ĵ���
    #     vector = np.array(voca_dict[feature_name][voca_index].fillna(0))
    #     #print("vector.nonzero():",vector.nonzero())
    #     return vector

        # x_voca = []
        # for i in eval(x):
        #     voca = voca_dict.index[int(i)-1]
        #     if int(i) == 0:  #ע����һ���ֵ��Ȼ��NULL�����ﵥ���г������滻Ϊ�ˡ�������
        #         x_voca.append(0)
        #     else:
        #         x_voca.append(voca_dict[feature_name][voca])  #�����nan��pandas�޷�ʶ��
        # return x_voca


    print("begin transfer to "+feature_name+" vector....")
    pd_train['class'] = pd_train['class'].apply(eval)
    pd_test['class'] = pd_test['class'].apply(eval)
    pd_train[feature_name] = pd_train['sequence'].apply(eval)
    pd_test[feature_name] = pd_test['sequence'].apply(eval)
    print("end transfer to "+feature_name+" vector.")

    # ����������
    #pd_test = pd_test.head(10)
    return (pd_train,pd_test,voca_dict)

def main(pd_data,voca_dict, k_num,flod_num,feature_name,evaluation_csv=None):
    # ����ÿ�����Լ�
    begin = time.time()
    kf_evaluation_result = knn.multi_flod(pd_data,voca_dict, k_num,flod_num,feature_name)
    end = time.time()
    print("result:",kf_evaluation_result)
    if evaluation_csv:
        kf_evaluation_result.to_csv(evaluation_csv,encoding="utf8")
    print("total time:", end - begin)

if __name__ == '__main__':
    #��������
    feature_name = "tf_idf"
    train_csv = sdp.TRAIN_BINARY_COMMENT
    test_csv = sdp.TEST_BINARY_COMMENT
    voca_csv = sdp.VOCA_BINARY_COMMENT
    evaluation_csv = sdp.EVALUATION_KNN_COMMENT

    pd_train, pd_test, voca_dict = get_binary_class_data(train_csv,test_csv,voca_csv,feature_name)
    pd_data = pd.concat([pd_train,pd_test],ignore_index=True)
    main(pd_data,voca_dict, K_LIST, FLOD_NUM, feature_name,evaluation_csv=evaluation_csv)