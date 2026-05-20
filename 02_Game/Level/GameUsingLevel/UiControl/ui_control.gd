extends CanvasLayer

@export var Login_System: PackedScene

var excel_path = "D:/GodotProject/Godot Excel Spreadsheet/godot-excel-spreadsheet/06_GameData/ServerData/GameDataExcel.xlsx"
var python_script = "res://06_GameData/ServerData/FileProcessingMain.py"

func _ready() -> void:
	_initialize()
	
# 初始化主菜单
func _initialize() -> void:
	# 初始化登录系统
	if not LoginSystem.get_login_state():
		var login_system = Login_System.instantiate()
		add_child(login_system)
		
