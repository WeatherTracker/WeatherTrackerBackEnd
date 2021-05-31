from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import SignatureExpired, BadSignature
import binascii 
from pyDes import des, CBC, PAD_PKCS5 
def create_confirm_token(mail,password,FCMToken,expires_in=600):
    SECRET_KEY = "FISTBRO"
    """
    利用itsdangerous來生成令牌，透過current_app來取得目前flask參數['SECRET_KEY']的值
    :param expiration: 有效時間，單位為秒
    :return: 回傳令牌，參數為該註冊用戶的id
    """
    secret_str = des_encrypt('FIST2021',password) 
    s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=expires_in)
    return s.dumps({'email': mail,'hash_password':str(secret_str),'FCMToken':FCMToken})

def create_token(mail,expires_in=36400):
    SECRET_KEY = "FISTBRO"
    """
    利用itsdangerous來生成令牌，透過current_app來取得目前flask參數['SECRET_KEY']的值
    :param expiration: 有效時間，單位為秒
    :return: 回傳令牌，參數為該註冊用戶的id
    """
    s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=expires_in)
    return s.dumps({'email': str(mail)})

def create_user_token(userId,expires_in=36400):
    SECRET_KEY = "FISTBRO"
    """
    利用itsdangerous來生成令牌，透過current_app來取得目前flask參數['SECRET_KEY']的值
    :param expiration: 有效時間，單位為秒
    :return: 回傳令牌，參數為該註冊用戶的id
    """
    s = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=expires_in)
    return s.dumps({'userId': str(userId)})

def des_decrypt(secret_key, s): 
        iv = "DONTSTOP"
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5) 
        de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5) 
        return de 

def des_encrypt(secret_key, s): 
    iv = "DONTSTOP"
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5) 
    en = k.encrypt(s, padmode=PAD_PKCS5) 
    return binascii.b2a_hex(en) 
def decode_token(token):
    s = TimedJSONWebSignatureSerializer('FISTBRO', expires_in=36400)
    try:
        token=token.split('\'')[1] 
        data = s.loads(token)  # 驗證
        encodedId=data.get('userId')
        # print("在decode裡面的 encodedId",encodedId)
        # userId=des_decrypt("FIST2021",encodedId)
        # print("在decode裡面的userId",type(userId))
        return encodedId
    except Exception as e:
        print(e)
        return "False"
