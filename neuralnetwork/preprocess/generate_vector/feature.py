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
    voca_dict[feature_name] = df_bdc_set

def getTFRF(voca_dict,classnum,feature_name):
    """
    ���tf rfֵ��ע��tf��voca�����Դ��ģ�tf�Ǵ������Ͽ��е�Ƶ�ʣ�idf��log(N/(a+c))��a�Ǵ����������ĵ�����c�Ǵ��ڸ������ĵ���
    word_appear_set,class_word_appear_set,word_doc_set,doc_class_set
    :param voca_dict:�ֵ��б�������tf��dataframe
    :param classnum:���ٷ��࣬��ʵ������Ѿ��̶���Ϊ�����࣬�����Ҫ��Զ���࣬��Ҫ��c����Ľ�
    :param feature_name:��Ҫ�洢���б���
    :return:����
    """
    print("begin get tf rf.")
    count = 0
    voca_dict[feature_name] = range(len(voca_dict))  #Ԥռλ
    def f(row):
        #print("row is:",row)
        return row['tf'] * math.log(
            2 + float(row['word_doc_set'][0]) / max(1, float(row['word_doc_set'][1])))
    # for index, row in voca_dict.iterrows():
    #     print(row)
    #     count += 1
    #     if count%100 == 0:
    #         print("tf idf------has get count:",count)
    #     voca_dict[feature_name][index] = row['tf']*math.log(
    #         2+float(row['word_doc_set'][0])/max(1,float(row['word_doc_set'][1])))

    voca_dict[feature_name] = voca_dict.apply(f,axis=1)

    print("end get tf idf.")



def getTFIDF(voca_dict,classnum,feature_name):
    """
    ���tfidfֵ��ע��tf��voca�����Դ��ģ�tf�Ǵ������Ͽ��е�Ƶ�ʣ�idf��log(N/(a+c))��a�Ǵ����������ĵ�����c�Ǵ��ڸ������ĵ���
    word_appear_set,class_word_appear_set,word_doc_set,doc_class_set
    :param voca_dict:�ֵ��б�������tf��dataframe
    :param classnum:���ٷ��࣬��ʵ������Ѿ��̶���Ϊ�����࣬�����Ҫ��Զ���࣬��Ҫ��c����Ľ�
    :param feature_name:��Ҫ�洢���б���
    :return:����
    """
    print("begin get tf idf.")
    count = 0
    voca_dict[feature_name] = range(len(voca_dict))  # Ԥռλ
    def f(row):
        #print("row is:",row)
        return row['tf'] * math.log(
             float(sum(row['doc_class_set'])) / float(sum(row['word_doc_set'])))
    # for index, row in voca_dict.iterrows():
    #     count += 1
    #     if count%100 == 0:
    #         print("tf idf------has get count:",count)
    #     voca_dict[feature_name][index] = row['tf'] * math.log(
    #         float(sum(row['doc_class_set'])) / float(sum(row['word_doc_set'])))

    voca_dict[feature_name] = voca_dict.apply(f,axis=1)

    print("end get tf idf.")
