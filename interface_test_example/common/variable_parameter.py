# variable_parameter.py
__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'

API = {
    "inbound": "/api/warehouse/warehouse/editOrderInfo/",
}
# 维修方法：1-维修，2-更换，3-补充，5-升级
REPAIR_METHOD = [1, 2, 3, 5]

# 图片链接 一个图片一个视频
FILE_PATH = "https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/114212_1OIP-C.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/152207_test video.mp4"
# 两张图片
FILE_PATH_TWO = "https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/114212_1OIP-C.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/152326_test.jpg"
# 维修添加部件的图片，只能是图片4张
REPAIR_FILE_PATH = "https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162203_ANJT-jtb.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162246_ModelYMaterial.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162254_Rivet.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162304_一字螺丝刀.png"

# 维修检测步骤码
STEP_CODE = "new_base_info"

# 维修检测备注
REPAIR_CHECK_NOTE = "自动化测试维修检测备注"
REPAIR_TYPE_REJECTS = 3
REPAIR_TYPE_GOOD = 5

# 维修类型
SERVICE_TYPE = 1

