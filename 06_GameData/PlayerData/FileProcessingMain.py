from openpyxl.worksheet.worksheet import Worksheet
from ExcelProcessing import read_from_excel
from ExcelProcessing import write_new_account
from ExcelProcessing import detect_id_excel_exist
from JsonProcessing import convert_excel_to_account
from JsonProcessing import detect_login_information
from JsonProcessing import convert_excel_to_dir
from JsonProcessing import convert_dir_to_json
from typing import Optional
import os
import sys

#=============默认存档名============#
default_save_exc_name       = "GameDataExcel.xlsx"
default_exc_data_player     = "PlayerData"
default_json_out            = "PlayerGameData.json"
#=============默认存档名============#

"""
一下所有函数面向Godot返回
全部使用print
"""
# 登录验证器
def login_verify(input_login_info: Optional[list[str]]) -> None:
    if input_login_info is None:
        return None
    
    try:
        # 得到账户表格
        read_sheet = read_from_excel(default_save_exc_name, default_exc_data_player)
        stored_info_dict = convert_excel_to_account(read_sheet)
        # 验证登录信息
        verify_result: tuple =  detect_login_information(stored_info_dict, input_login_info)
        # 通过验证
        print(verify_result[1])
    except Exception as e:
        # 登录程序运行失败
        print("-1")

# 注册验证器
def register_verify(input_register_info: Optional[list[str]]) -> None:
    if input_register_info == None:
        return None
    
    try:
        # 验证注册信息并写入
        varify_result: tuple = write_new_account(default_exc_data_player, 
                                                 default_save_exc_name, 
                                                 input_register_info)
        print(varify_result[1])

    except Exception as e:
        # 注册程序运行失败
        print("-1")

# 主函数进入
if __name__ == "__main__":

    if len(sys.argv) >= 4:
        # 获得传入excel地址参数
        default_save_exc_name = sys.argv[1]
        
        # 检查文件路径
        if not os.path.exists(default_save_exc_name):
            print(f"路径: {default_save_exc_name} 不存在")
        # 尝试进行账号操作      
        else:
            try:

                read_sheet = read_from_excel(default_save_exc_name, default_exc_data_player)
                result_dir = convert_excel_to_account(read_sheet)
            
            # 错误处理
            except Exception as e:
                print(f"操作异常: {e}")