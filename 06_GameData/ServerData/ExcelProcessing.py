from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from openpyxl import load_workbook
from typing import Optional

DEBUG = False
# 调试信息输出
def log(msg):
    """只有 DEBUG=True 时才打印，否则不输出任何东西"""
    if DEBUG:
        print(msg)

"""
Excel优化体
后续完成后可以考虑优化
"""
#===============全局文件管理器Excel===============#
"""
统一管理全局被打开的Excel
防止手动释放出现问题
"""
class Excel_Manager:
    inner_excel: Workbook

    # 默认空表
    def __init__(self):
        self.inner_excel: Workbook      = None

    # 尝试全局创建打开Excel
    def open_excel(self, file_path: str) -> bool:
        # 检查存在
        if self.inner_excel:
            log(f"打开对象已存在: {self.inner_excel}: 请手动释放")
            return False

        # 尝试读取
        try:
            # 获取Excel
            read_excel: Workbook = load_workbook(file_path, read_only=True)
            self.inner_excel = read_excel
            return True
        # 异常处理
        except Exception as e:
            log(f"打开Excel发生异常: {e}")
            return False

    # 获得类中Excel
    def get_excel(self) -> Optional[Workbook]:
        # 检查存在
        if self.inner_excel:
            log(f"成功返回Excel: {self.inner_excel}")
            return self.inner_excel
        # 不存在
        log("返回excel失败,excel并未读取")
        return None

    # 获得表单   
    def get_sheet(self, sheet_name: str) -> Optional[Worksheet]:
        # 检查存在
        if not self.inner_excel:
            log("不存在原表")
            return None

        # 返回特定表     
        try:
            if sheet_name not in self.inner_excel.sheetnames:
                log(f"工作表'{sheet_name}' 不存在")
                return None
            # 返回表
            return self.inner_excel[sheet_name]
        except Exception as e:
            log(f"表单返回发生异常: {e}")
            return None

    # 关闭表格
    def close_workbook(self) -> bool:
        # 检查存在
        if not self.inner_excel:
            log("不存在原表,已经关闭")
            return True
        try:
            self.inner_excel.close()
            return True
        # 表单关闭失败
        except Exception as e:
            log(f"关闭excel出现异常: {e}")
            return False   
"""
以下为原版表格
需要注意表格的状态
开启或者关闭
"""

# 从excel中读取固定格式函数
def read_from_excel(file_read_path: str,
                    read_data_name: str,
                    read_only_out: bool = False) -> Optional[Worksheet]:
    
    # 返回指定列
    try:
        # 获取Excel
        read_excel: Workbook = load_workbook(file_read_path, read_only=read_only_out)
        if read_data_name not in read_excel.sheetnames:
            log(f"工作表'{read_data_name}' 不存在")
            read_excel.close()
            return None
        # 读取列
        read_excel_sheet = read_excel[read_data_name]
        read_excel.close()
        return read_excel_sheet
    # 读取失败
    except Exception as e:
        log(f"read failed{e}")
        # 打开了就关闭Excel
        if read_excel:
            read_excel.close()
        return None
    
"""
账户注册处理
返回-1: 程序运行出错
返回0 : 注册成功
返回1 : 账户注册出现问题(非法字符/账户密码问题)
返回2 : 账户已被注册
"""    
# 插入新玩家数据
def write_new_account(read_data_name: str,
                      file_read_path: str,
                      new_account_information: Optional[list[str]]) -> tuple[bool, int]:

    # 传入空列表处理
    if new_account_information is None:
        return False, -1

    get_account_verify: tuple[bool, str] = verify_account_data(new_account_information)
    if not get_account_verify[0]:
        log("账号登录或注册出现问题: " + get_account_verify[1])
        return False, 1

    # 尝试修改表格
    try:
        # 检查玩家ID重复
        if detect_id_excel_exist(read_data_name, file_read_path, new_account_information[0]):
            log(f"玩家ID已经存在: {new_account_information[0]}")
            return False, 2
    
        # 修改不能开 read_only=True
        read_excel: Workbook = load_workbook(file_read_path, read_only=False)
        if read_data_name not in read_excel.sheetnames:
            log(f"工作表'{read_data_name}' 不存在")
            read_excel.close()
            return False, -1
        
        # 选中工作表，获得新数据行号
        read_excel_sheet = read_excel[read_data_name]
        new_row_index = read_excel_sheet.max_row + 1
        col_num = read_excel_sheet.max_column

        # 数据不全全部补"None"
        need_add_num = col_num - len(new_account_information)
        if need_add_num > 0:
            new_account_information += [None] * need_add_num

        # 遍历新行单元格写入
        for col_index, input_value in enumerate(new_account_information, start=1):
            read_excel_sheet.cell(row=new_row_index, 
                                  column=col_index, 
                                  value=input_value)

        # 保存修改数据
        read_excel.save(file_read_path)
        read_excel.close()
        log(f"数据写入成功: {new_account_information} -> {file_read_path}")
        return True, 0


    # 写入失败处理
    except Exception as e:
        log(f"write failed: {e}")
        if read_excel:
            read_excel.close()
        return False, -1

# 查找玩家Id存在
def detect_id_excel_exist(read_data_name: str, file_read_path: str, detected_id: str) -> bool:
    # 尝试寻找ID
    try:
        # read_only=False，这样才可以使用列迭代器
        read_excel: Workbook = load_workbook(file_read_path, read_only=False)
        if read_data_name not in read_excel.sheetnames:
            log(f"工作表'{read_data_name}' 不存在")
            read_excel.close()
            return False
        
        # 选中工作表，获取最大行数
        read_excel_sheet = read_excel[read_data_name]
        read_sheet_first = read_excel_sheet["A"]
        row_max_len = read_excel_sheet.max_row

        # 遍历确认玩家ID不存在
        exist_dir: dict[str, int] = {}
        for current_row, cell in enumerate(read_sheet_first, start=1):
            # 略过第一个属性名
            if current_row == 1:
                continue
            # 放入字典
            if cell.value:
                exist_dir[str(cell.value)] = 1

        # 对比检测是否存在
        if detected_id in exist_dir:
            read_excel.close()
            return True
        read_excel.close()
        return False

    except Exception as e:
        log(f"查找Excel出现问题: {e}")
        if read_excel:
            read_excel.close()
        return False
    
# 传入账号信息合法性校验
def verify_account_data(acc_info: list[str]) -> tuple[bool, str]:
    """
    账号合法性质校验、
    校验至少[账号ID, 密码, ......]
    """
    if not acc_info or len(acc_info) < 2:
        return False, "字段不足: 至少需要[账号ID, 密码]"
    
    acc_id          = acc_info[0]
    acc_password    = acc_info[1]

    # 账号基本信息校验
    if not acc_id:
        return False, "账号ID不能为空或全空格"
    if len(acc_id) < 3:
        return False, "账号长度不能小于3"
    if any(per_char in r'\/:*?"<>| ' for per_char in acc_id):
        return False, "账号ID包含非法特殊字符"
    
    # 密码校验
    if not acc_password:
        return False, "密码不能为空"
    if len(acc_password) < 4:
        return False, "密码长度不能小于4"
    
    return True, "校验通过"