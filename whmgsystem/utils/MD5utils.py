import hashlib

def getMD5(restr):
    '''
    获取strmd5
    :param restr:
    :return:
    '''
    MD5 = hashlib.md5()
    MD5.update(restr.encode("utf8"))
    return MD5.hexdigest()