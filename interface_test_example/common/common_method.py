import string
import random

# 获取指定长度的随机数字字符串
def get_random_data_number(num):
    return ''.join(random.choices(string.digits, k=num))

# 获取指定长度的随机字母数字字符串
def get_random_data_alphanumeric(num):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num))