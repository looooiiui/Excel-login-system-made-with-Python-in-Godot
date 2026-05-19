extends Node2D

@export var Login		: Node2D
@export var Register	: Node2D

var excel_path = "D:/GodotProject/Godot Excel Spreadsheet/godot-excel-spreadsheet/06_GameData/ServerData/GameDataExcel.xlsx"
var python_script = "res://06_GameData/ServerData/FileProcessingMain.py"

# 获得默认python脚本路径
func get_python_processing_path() 	-> String:
	return python_script
	
# 获得默认excel路径
func get_excel_path() 				-> String:
	return excel_path

# 进行登录验证(返回诸如"0", "1")
func login_verify(name: String, password: String)		-> String:
	# 改为标准格式
	var input_info: Array[String] = [name, password]
	var verify_result = Login.login_info_verify(input_info)
	return verify_result
		
	
