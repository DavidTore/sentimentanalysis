# coding=gbk
import math
import types
"""
    ����bdcֵ������������ֵ
"""
def __getOriginalValue(value):
    if type(value) == types.StringType:
        return eval(value)
    else:
        return value

#���ݴʵ����BDCֵ��voca_dict�ĸ�ʽΪpandas dataframe
def getBDCVector(voca_dict,classnum,feature_name):
    bdc_set = []
    # word_num[0]Ϊ���ʣ���ÿ���ʶ���
    for index, row in voca_dict.iterrows():
        posibility_list = []  #����ÿ�����еĸ���
        # ��ÿ���������
        for j in range(classnum):
            #__getOriginalValue��strתΪlist����������Ϊpandas���ļ��ж�ȡdataframeʱlist����str
            posibility_list.append(float(__getOriginalValue(row['word_appear_set'])[j]) / float(__getOriginalValue(row['class_word_appear_set'])[j]))
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
            posibility_list.append(
                float(__getOriginalValue(row['word_doc_set'])[j]) / float(__getOriginalValue(row['doc_class_set'])[j]))
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

#�����Լ��в����ڵ�������Ӧ��Ϊ0
def getTotalVoca(pd_test,voca_dict):
    # ��pd_test�е���������voca_dict�У�����������У�Ӧ�ý�voca_dict�ж�Ӧ����ȫ��ֵ����Ϊ0
    for line in pd_test['content']:
        for word in line:
            if word not in voca_dict.index:
                voca_dict.loc[word] = 0  #��Ӷ�Ӧ������



def getTFRF(voca_dict,classnum,feature_name):
    """
    ���tf rfֵ��ע��tf��voca�����Դ��ģ�tf�Ǵ������Ͽ��е�Ƶ�ʣ�idf��log(N/(a+c))��a�Ǵ����������ĵ�����c�Ǵ��ڸ������ĵ���
    word_appear_set,class_word_appear_set,word_doc_set,doc_class_set
    :param voca_dict:�ֵ��б�������tf��dataframe
    :param classnum:���ٷ��࣬��ʵ������Ѿ��̶���Ϊ�����࣬�����Ҫ��Զ���࣬��Ҫ��c����Ľ�
    :param feature_name:��Ҫ�洢���б���
    :return:����
    """
    voca_dict[feature_name] = range(len(voca_dict))  #Ԥռλ
    for index, row in voca_dict.iterrows():
        voca_dict[feature_name][index] = row['tf']*math.log(
            2+float(row['word_doc_set'][0])/max(1,float(row['word_doc_set'][1])))


def getTFIDF(voca_dict,classnum,feature_name):
    """
    ���tfidfֵ��ע��tf��voca�����Դ��ģ�tf�Ǵ������Ͽ��е�Ƶ�ʣ�idf��log(N/(a+c))��a�Ǵ����������ĵ�����c�Ǵ��ڸ������ĵ���
    word_appear_set,class_word_appear_set,word_doc_set,doc_class_set
    :param voca_dict:�ֵ��б�������tf��dataframe
    :param classnum:���ٷ��࣬��ʵ������Ѿ��̶���Ϊ�����࣬�����Ҫ��Զ���࣬��Ҫ��c����Ľ�
    :param feature_name:��Ҫ�洢���б���
    :return:����
    """
    voca_dict[feature_name] = range(len(voca_dict))  # Ԥռλ
    for index, row in voca_dict.iterrows():
        voca_dict[feature_name][index] = row['tf'] * math.log(
            sum(float(row['doc_class_set'])) / sum(float(row['word_doc_set'])))