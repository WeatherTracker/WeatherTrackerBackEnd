from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import SignatureExpired, BadSignature
def create_confirm_token(self, expires_in=3600):
    SECRET_KEY = "FISTBRO"
    """
    利用itsdangerous來生成令牌，透過current_app來取得目前flask參數['SECRET_KEY']的值
    :param expiration: 有效時間，單位為秒
    :return: 回傳令牌，參數為該註冊用戶的id
    """
    s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=expires_in)
    return s.dumps({'id': self})