extends Node2D

var excel_path = "D:/GodotProject/Godot Excel Spreadsheet/godot-excel-spreadsheet/06_GameData/ServerData/GameDataExcel.xlsx"
var python_script = "res://06_GameData/ServerData/FileProcessingMain.py"

func _ready() -> void:
	
	LoginSystem.login_verify("10400", "1")
