import pandas as pd

# 读取Excel文件，指定引擎
try:
    df = pd.read_excel(r'C:\Users\Administrator\Desktop\github\250526\code\interface_test_example\caseFile\excel\客户端普通维修单入库.xlsx', engine='openpyxl')
    print("Excel表头:")
    print(df.columns.tolist())
    print("\n前5行数据:")
    print(df.head())
except Exception as e:
    print(f"无法读取Excel文件: {e}")