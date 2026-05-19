from openpyxl.worksheet.worksheet import Worksheet
from typing import Optional
import json
import os

DEBUG = False
# 调试信息输出
def log(msg):
    """只有 DEBUG=True 时才打印，否则不输出任何东西"""
    if DEBUG:
        print(msg)

# 转换工作表为字典(默认字典格式，所有标题散装)
def convert_excel_to_dir(out_excel_worksheet: Optional[Worksheet]) -> dict[str, list[str]]:
    # 传值判断
    if out_excel_worksheet is None:
        log("默认字典转换: 传入的是空表")
        return {}
    
    try:
        # 转换标题列表
        excel_title_name: list[str | None]  = [str(cell.value) if cell.value is not None 
                                               else "None"
                                               for cell in out_excel_worksheet[1]]
        
        excel_value: list[str | int | None] = [cell.value if cell.value is not None
                                               else "None"
                                               for cell in out_excel_worksheet[2]]
        
        excel_zip_result = zip(excel_title_name, excel_value)
        # 元组转换字典
        excel_zip_to_dir = dict(excel_zip_result)
        # 返回字典
        return excel_zip_to_dir
    # 转换失败
    except Exception as e:
        log(f"Excel转换字典失败: {str(e)}")
        return {}

# ===============================================================================#
# 转换工作表为账号格式 { 'id': [密码, 昵称] }
# 适配Godot本地登录，直接查字典即可完成账号校验
# ===============================================================================#
def convert_excel_to_account(out_excel_worksheet: Optional[Worksheet]) -> dict:
    # 传值判断
    if out_excel_worksheet is None:
        log("账号字典转换: 传入的是空表")
        return {}

    try:
        # 转换账户信息ID
        excel_id_list:          list[str | None]        = []
        excel_password_list:    list[str | None]        = []
        excel_name_list:        list[str | None]        = []
        excel_account_dir:      dict[str , list]         = {}
        # 添加数据内置函数
        def append_value(cell: tuple, excel_list: list):
            for cell_value in cell:
                    append_case: str = ""
                    # 防止添加None破坏数据稳定
                    if cell_value.value is None:
                        append_case = "None"
                    else:
                        append_case = str(cell_value.value)
                    # 添加玩家信息
                    excel_list.append(append_case)

        # 注意传进来的工作表不要 read_only=True
        for col_num, cell in enumerate(out_excel_worksheet.iter_cols(min_col=1, 
                                                                     max_col=3, 
                                                                     min_row=2, 
                                                                     max_row=None), 
                                       start=1):

            # 添加玩家信息到对应列表
            match col_num:
                # 玩家账户ID信息
                case 1:
                    append_value(cell, excel_id_list)
                # 玩家密码信息
                case 2: 
                    append_value(cell, excel_password_list)
                # 玩家名字信息
                case 3:
                    append_value(cell, excel_name_list)
                
        # 转换为字典
        min_valid_length = min(len(excel_password_list), len(excel_name_list), len(excel_id_list))
        # 截断列表
        excel_id_list           = excel_id_list[:min_valid_length]
        excel_name_list         = excel_name_list[:min_valid_length]
        excel_password_list     = excel_password_list[:min_valid_length]
        
        # 中间数组
        result_info_list: list[list[str]] = []
        # 整合结果字典 [[password, name]]
        result_info_list = [
            [password, name]
            for password, name in zip(excel_password_list, 
                                      excel_name_list)
        ]

        # 转换字典
        excel_account_dir = dict(zip(excel_id_list, result_info_list))
        return excel_account_dir
        
    # 账户字典转换失败          
    except Exception as e:
        log(f"账户字典创建失败: {str(e)}")
        return {}
#===============================================================================#

# 字典创建JSON文件
def convert_dir_to_json(out_dir: dict, json_out_path: str) -> None:
    # 尝试创建JSON文件
    try:
        convert_dir: str = json.dumps(
            out_dir, 
            ensure_ascii=False, 
            indent=4,
            sort_keys=False
            )
        # 写入JSON
        with open(json_out_path, "w", encoding="utf-8") as file:
            file.write(convert_dir)
        log(f"JSON文件创建成功: {json_out_path}")
    # 创建失败
    except Exception as e:
        log(f"字典创建JSON失败: {str(e)}")

# 校验登录信息
def detect_login_information(input_info_dict: dict, 
                             login_info: Optional[list[str]]
                             ) -> tuple[bool, int]:
    """
    校验玩家登录信息（账号 + 密码）
    
    返回值说明:
    - 元组第1位:是否校验通过(True=通过,False=不通过)
    - 元组第2位:状态码
      - 0 : 账号验证通过
      - 1 : 账户信息不存在
      - 2 : 账号信息验证错误（信息不全/密码错误）
    """

    if login_info is None:
        log("登录验证: 传入的是空信息")
        return False, 1

    # 校验输入长度
    if len(login_info) < 2:
        log("登录信息不全")
        return False, 2
    
    # 校验玩家ID存在
    if not (login_info[0] in input_info_dict):
        log("账号不存在!")
        return False, 1

    # 校验密码
    input_password = login_info[1]
    stored_password = input_info_dict[login_info[0]][0]
    if input_password != stored_password:
        log("账号密码错误!")
        return False, 2
        
    # 校验通过
    log("校验通过")
    return True, 0
    