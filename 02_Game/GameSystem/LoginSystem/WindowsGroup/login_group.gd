extends Control

@export var Login_Windows: 		Window
@export var Confirm_Button: 	Button

var user_state: GlobalEnum.User_State 			= GlobalEnum.User_State.LOGIN
var user_per_state: GlobalEnum.User_State 		= GlobalEnum.User_State.REGISTER
# 初始化
func _ready() -> void:
	_initialize()
	
# 用户操作状态检测
func _user_operator_detected() -> void:
	# 仅在用户切换状态的时候触发
	if (user_state == user_per_state):
		return
	
	# 状态检测
	match user_state:
		GlobalEnum.User_State.LOGIN:
			Login_Windows.title = "登录"
			Confirm_Button.text = "登录"	
		GlobalEnum.User_State.REGISTER:
			Login_Windows.title = "注册"
			Confirm_Button.text = "注册"	
	# 更新用户状态
	user_per_state = user_state
	
# 初始化
func _initialize() -> void:
	# 窗口初始化
	Login_Windows.visible = false
	_user_operator_detected()

"""
改变用户状态
状态 0 登录
状态 1 注册
"""
func change_user_state(state: int) -> void:
	match state:
		0: user_state = GlobalEnum.User_State.LOGIN
		1: user_state = GlobalEnum.User_State.REGISTER
	# 尝试更新一次状态
	_user_operator_detected() 

# 返回当前状态
func get_user_state() -> GlobalEnum.User_State:
	return user_state
