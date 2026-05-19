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

#=============指定参数==============#
default_order_index:            int = 2       # 这里是默认从godot获得的参数中取第2位为指令参数
default_excel_path_index:       int = 1       # 默认Excel位置
default_order_name_index:       int = 3       # 默认名字位置
default_order_pwd_index:        int = 4       # 默认密码位置
default_godot_argv_len:         int = 5       # 默认传参长度

"""
以下所有函数面向Godot返回
全部使用print
"""

"""
返回值说明:
- 元组第1位:是否校验通过(True=通过,False=不通过)
- 元组第2位:状态码
    - 0 : 账号验证通过
    - 1 : 账户信息不存在
    - 2 : 账号信息验证错误（信息不全/密码错误）
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
        print(str(verify_result[1]))
    except Exception as e:
        # 登录程序运行失败
        print("-1")

"""
账户注册处理
返回-1: 程序运行出错
返回0 : 注册成功
返回1 : 账户注册出现问题(非法字符/账户密码问题)
返回2 : 账户已被注册
"""
# 注册验证器
def register_verify(input_register_info: Optional[list[str]]) -> None:
    if input_register_info == None:
        return None
    
    try:
        # 验证注册信息并写入
        varify_result: tuple = write_new_account(default_exc_data_player, 
                                                 default_save_exc_name, 
                                                 input_register_info)
        print(str(varify_result[1]))

    except Exception as e:
        # 注册程序运行失败
        print("-1")
"""
返回 -1 为程序运行出错
返回 -2 为程序输入变量不足
"""
# 主函数进入
if __name__ == "__main__":
    if len(sys.argv) >= default_godot_argv_len:
        # 将Godot传参转至本地
        receive_params: list[str] = sys.argv
        godot_order = receive_params[default_order_index]
        # 格式化传参内容
        default_save_exc_name   = receive_params[default_excel_path_index]
        input_name              = receive_params[default_order_name_index]
        input_pwd               = receive_params[default_order_pwd_index] 
        input_login_info: list[str] = [input_name, input_pwd]
        # 登录验证请求
        if (godot_order == "0"):
            login_verify(input_login_info)

    else:
        print("-2")