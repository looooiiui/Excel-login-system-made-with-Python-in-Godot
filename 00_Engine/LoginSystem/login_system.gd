extends Node2D

# 登录检测信号
signal login_success
signal login_out

@export var Login		: Node2D
@export var Register	: Node2D

# 存储当前账号状态
var current_account_id: String 	= ""
var is_Login: bool 				= false

var excel_path = "D:/GodotProject/Godot Excel Spreadsheet/godot-excel-spreadsheet/06_GameData/ServerData/GameDataExcel.xlsx"
var python_script = "res://06_GameData/ServerData/FileProcessingMain.py"

# 获得默认python脚本路径
func get_python_processing_path() 	-> String:
	return python_script
	
# 获得默认excel路径
func get_excel_path() 				-> String:
	return excel_path

"""
以下登录返回值类型
返回 0 登录成功
返回 1 账户信息不存在
返回 2 账户信息验证错误(密码错误)
"""
# 进行登录验证(返回诸如"0", "1")
func login_verify(name: String, password: String)		-> String:
	# 改为标准格式
	var input_info: Array[String] = [name, password]
	var verify_result = Login.login_info_verify(input_info)
	
	# 登录器自验证注册是否成功
	verify_login_success(verify_result, name)
	return verify_result

"""
以下注册返回值类型
返回 0 注册成功
返回 1 账户注册出现问题(非法字符/账户密码问题)
返回 2 账户已被注册
"""		
# 进行注册验证
func register_verify(name: String, password: String)	-> String:
	# 改为标准格式
	var input_info: Array[String] = [name, password]
	var verify_result = Register.register_info_verify(input_info)
	
	# 登录器自验证注册是否成功
	verify_login_success(verify_result, name)
	return verify_result

# 获得当前登录玩家ID
func get_current_id() -> String:
	return current_account_id
	
# 更改当前玩家登录ID
func change_current_id(new_id: String) -> void:
	current_account_id = new_id

# 获得登录状态
func get_login_state() -> bool:
	return is_Login

# 登录成功验证
func verify_login_success(verify_result: String, verift_account_name: String) -> void:
	if verify_result == "0":
		is_Login = true
		login_success.emit()
	
	# 成功更新服务器信息
	if is_Login:
		current_account_id = verift_account_name

# 退出登录
func exit_login() -> void:
	is_Login = false
	current_account_id = ""
	login_out.emit()
