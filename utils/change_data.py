# coding=gbk

"""
    ����ת��
"""
def getOriginalValue(value):
    """
    ���ַ�������ת����ע��eval("ac")��ac���δ��ǰ������ᱨ��
    :param value: һ�����ݣ�str������
    :return: ������ַ��������ת��
    """
    if type(value) == str:
        value = eval(value)
        while Ellipsis in value:
            value.remove(Ellipsis)
        return value
    else:
        return value