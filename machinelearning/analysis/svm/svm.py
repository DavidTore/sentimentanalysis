# coding=gbk
from sklearn import svm
import pandas as pd
import numpy as np
"""
    SVM��ʵ��
"""
def svm_classification(train_data,train_target,test_data,test_target):
    clf = svm.SVC()
    clf.fit(train_data,train_target)

    result = clf.predict(test_data)

    return np.array([test_target,result]).T

def evaluation_binaryclass(result_data):
    """
    ����������������Ĭ��class��һ����1Ϊ���࣬�ڶ�����1Ϊ����
    :param result_data: knn���صĽ������[test1[right,predict[k1,k2,k3]],test2[]]
    :param k_list: k list
    :return: [k1[p,r,f1],k2[p,r,f1],k3...]
    """
    print("classification result:",result_data)
    tp, fn, fp, tn = 0, 0, 0, 0
    for j in range(len(result_data)):
        # result_data[j][0]Ϊ��ʵ��ǣ�result_data[j][1][k]Ϊ��K��Ԥ���ǣ���ֻ��0��1���֣�0Ϊ������0����Ϊ1����1Ϊ������1����Ϊ1��
        if result_data[j][0] == 0 and result_data[j][1] == 0:  # ��ʵ==Ԥ��==��
            tp += 1
        if result_data[j][0] == 0 and result_data[j][1] == 1:  # ��ʵΪ����Ԥ��Ϊ��
            fn += 1
        if result_data[j][0] == 1 and result_data[j][1] == 0:  # ��ʵΪ����Ԥ��Ϊ��
            fp += 1
        if result_data[j][0] == 1 and result_data[j][1] == 1:  # ��ʵΪ����Ԥ��Ϊ��
            tn += 1
    if tp + fp == 0:
        precision = float(0)
    else:
        precision = float(tp) / (tp + fp)
    if tp + fn == 0:
        recall = float(0)
    else:
        recall = float(tp) / (tp + fn)
    if precision + recall == 0:
        f1 = float(0)
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return pd.DataFrame([precision, recall, f1])
