extends VBoxContainer

@export var Login_Window		: Window
@export var Login_Group			: Control

func _ready() -> void:
	_initialize()

# 登录按键
func _on_login_pressed() -> void:
	Login_Window.visible = true
	Login_Group.change_user_state(0)

# 注册按键
func _on_register_pressed() -> void:
	Login_Window.visible = true
	Login_Group.change_user_state(1)
	
func _on_exit_game_pressed() -> void:
	get_tree().quit()
	
# 初始化
func _initialize() -> void:
	# 窗口初始化
	Login_Window.visible = false
