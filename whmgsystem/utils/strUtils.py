def isLegal(s):
    '''
    判断字符串是否为空或含有空格
    :param s: 字符串
    :return: 含有空返回false
    '''
    if s ==None:
        return False
    elif ' ' in s:
        return False
    elif s=='':
        return False
    return True
def isLegals(lists):
    '''
    判断多个字符串是否含有空或为空
    :param lists: 字符串list
    :return: 含有空返回false
    '''
    for l in lists:
        if isLegal(l)==False:
            return False
    return True