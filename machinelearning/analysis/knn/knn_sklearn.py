# coding=gbk
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.cross_validation import KFold
from sklearn.metrics.pairwise import cosine_similarity

def calDistance(pd_data,voca_dict,feature_name):
    """
    ��������֮���cos���ƶ�
    :param pd_data: �������ݼ�
    :param feature_name: ��Ӧ��������
    :return: �������ƶȾ���
    """
    ans = []
    for index,vector in pd_data.iterrows():
        temp = np.array(vector[feature_name]) * np.array(voca_dict[feature_name])
        ans.append(temp)

    sparseMatrix = sparse.csr_matrix(ans)   #תΪϡ�����
    similarities = cosine_similarity(sparseMatrix)
    print(similarities)
    return similarities


def knn_core(test_index,train_set,k_list):
    """
    knn����ĺ��ģ�����ÿ�����Լ�����
    :param test_index: �������ݶ�Ӧ��index������ʵ�����ǵ���
    :param train_set: ѵ������������ѵ�����Ͳ��Լ������ƶȾ�����������иĽ��Ŀռ䣬��Ϊtrain_set�Ƕ�Ӧ���еĲ��Լ�
    :param k_list: ȡ����Ӧ��k��ֵ��������Ҫ�Ľ���Ӧ�ÿ���ȡ����Ӧ��k������ֱ����range(k)
    :return:
    """
    new_set = sorted(train_set, key=lambda file: file[2][test_index],reverse=True)
    #get top k list
    answer = []
    for k in k_list:
        topk_set = np.array([true_class[1] for true_class in new_set[0:k]])
        #ֱ��sum topk_set
        answer.append(topk_set.sum(0).argmax())  #�������ֵ���ڵ�index��0��ʹ���࣬1���Ǹ���
    return answer

def knn(train_index, test_index, distance, pd_data, k_list):
    """
    ����ѵ�����Ǳ꣬���Լ��Ǳ꣬�������ģ������KNN�㷨
    :param train_index: ѵ�����Ǳ꣬list
    :param test_index:  ���Լ��Ǳ꣬list
    :param distance: �������
    :param pd_data: ���ݼ���������Ҫȡ����Ӧ����ʵ��ǩ��'class'
    :param k_list: ȡ����Ӧ��k��ֵ
    :return: ��ƽ��΢ƽ��
    """
    ans_set = []
    #ȡ����Ӧ����ʵ��ǩ�;������ֵ
    train_set = [[index,pd_data['class'][index],distance[index]] for index in train_index]

    #����ÿ�����Լ�����
    for i in range(len(test_index)):
        result = knn_core(test_index[i], train_set,k_list)  #�Բ��Լ����з��࣬1�����࣬0������
        ans_set.append([pd_data['class'][i].index(1),result])   #��ʵ�����ڵ�index���Լ�Ԥ��������ڵ�index

    return ans_set

def evaluation_binaryclass(result_data,k_list):
    """
    ����������������Ĭ��class��һ����1Ϊ���࣬�ڶ�����1Ϊ����
    :param result_data: knn���صĽ������[test1[right,predict[k1,k2,k3]],test2[]]
    :param k_list: k list
    :return: [k1[p,r,f1],k2[p,r,f1],k3...]
    """
    print("classification result:",result_data)
    evaluation_result = []
    for k in range(len(k_list)):
        tp, fn, fp, tn = 0, 0, 0, 0
        for j in range(len(result_data)):
            # result_data[j][0]Ϊ��ʵ��ǣ�result_data[j][1][k]Ϊ��K��Ԥ���ǣ���ֻ��0��1���֣�0Ϊ������0����Ϊ1����1Ϊ������1����Ϊ1��
            if result_data[j][0] == 0 and result_data[j][1][k] == 0:  # ��ʵ==Ԥ��==��
                tp += 1
            if result_data[j][0] == 0 and result_data[j][1][k] == 1:  # ��ʵΪ����Ԥ��Ϊ��
                fn += 1
            if result_data[j][0] == 1 and result_data[j][1][k] == 0:  # ��ʵΪ����Ԥ��Ϊ��
                fp += 1
            if result_data[j][0] == 1 and result_data[j][1][k] == 1:  # ��ʵΪ����Ԥ��Ϊ��
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
            f1 = 2*precision*recall/(precision+recall)
        evaluation_result.append([precision,recall,f1])
    return evaluation_result


def multi_flod(pd_data,voca_dict,k_list,flod_num,feature_name):
    """
    ���۽���ʵ�飬����pandas dataframe������k_list p/r/f1
    :param pd_data: pandas dataframe��binary����
    :param voca_dict: �ֵ��б�����weighting
    :param k_list: knn�е�k list
    :param flod_num: n�۽���ʵ�鷨
    :param feature_name: ��Ҫ�����������tfidf/tfrf/bdc
    :return: 
    """
    distance = calDistance(pd_data,voca_dict,feature_name)  #�������
    kf = KFold(len(pd_data), n_folds=flod_num)
    kf_evaluation_result = []   #[flod1[k1[p,r,f1],k2[p,r,f1],k3[p,r,f1]],flod2[k1,k2,k3]]
    for train_index, test_index in kf:  #����ÿһ��ʵ��
        ans_set = knn(train_index, test_index,distance,pd_data, k_list)
        kf_evaluation_result.append(evaluation_binaryclass(ans_set,k_list))  #���������ɸ�K��[k1[p,r,f1],k2[p,r,f1],k3[p,r,f1]]

    # each flod and each k
    kf_evaluation_result = np.array(kf_evaluation_result).T  #[p[k1[flod1,flod2],k2[flod1,flod2]],r[],f1[]]
    kf_evaluation_result = np.array([i.sum(1) for i in kf_evaluation_result]).T   #[k1[p_av,f_av],k2[p_av,f_av]]
    return pd.DataFrame(kf_evaluation_result)