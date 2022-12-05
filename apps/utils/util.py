import json

from Crypto.Cipher import AES
from base64 import b64encode, b64decode






class Aescrypt:
    def __init__(self):
        self.key = '0CoJUm6Qyw8W8jud'
        self.iv = '1234567812345678'
        self.mode = AES.MODE_CBC
        self.BLOCK_SIZE = AES.block_size
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s.encode()) % self.BLOCK_SIZE) * chr(
            self.BLOCK_SIZE - len(s.encode()) % self.BLOCK_SIZE)
        # 去除补位
        self.un_pad = lambda s: s[:-ord(s[len(s) - 1:])]
        # 不足BLOCK_SIZE的补位(s可能是含中文，而中文字符utf-8编码占3个位置,gbk是2，所以需要以len(s.encode())，而不是len(s)计算补码)

    def encrypt_aes(self, a_text):
        """
        加密 ：先补位，再AES加密，后base64编码
        :param text: 需加密的明文
        :return:
        """
        # text = pad(text) 包pycrypto的写法，加密函数可以接受str也可以接受bytess
        text = self.pad(a_text).encode()  # 包pycryptodome 的加密函数不接受str
        cipher = AES.new(key=self.key.encode(), mode=self.mode, IV=self.iv.encode())
        encrypted_text = cipher.encrypt(text)
        # 进行64位的编码,返回得到加密后的bytes，decode成字符串
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt_aes(self, encrypted_text):
        """
        解密 ：偏移量为key[0:16]；先base64解，再AES解密，后取消补位
        :param encrypted_text : 已经加密的密文
        :return:
        """
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(key=self.key.encode(), mode=self.mode, IV=self.iv.encode())
        decrypted_text = cipher.decrypt(encrypted_text)
        return self.un_pad(decrypted_text).decode('utf-8')


if __name__ == '__main__':
    aescrypt = Aescrypt()  # CBC模式
    # text = "456123qwe1胡成3213强大的"
    data_List = 35.0
    data_List = json.dumps(data_List, ensure_ascii=False)
    en_text = aescrypt.encrypt_aes(data_List)
    print(en_text)
    en_text1 = aescrypt.encrypt_aes(
        json.dumps({"datas": [], "version": "35.1"}, ensure_ascii=False))
    print("加密结果:", en_text1)
    # text = aescrypt.decrypt_aes("sDgAevgfqgzHMy1L3q6lmg==")
    # print("解密原文:", text)
    text = aescrypt.decrypt_aes("OVPFuxnsqkZveuE5kvsAtw43ss06Tafi4p7eAEwZkOSge+VnLun9o4Jk+NZJ9yuq8vh4szVvTNH5VSqnChq+3FgMYT8aMWTVuowtPZ5x+SUfuiYMuztYs4GCqjmE/puMxMLYRvk15yomdS2YPC6OGQzK0XCoDiUy+t/WlCyEWkU3vUMT9920QMtAsTb3gxjP")
    print("解密原文:", text)
