extends VBoxContainer

@export var Login_Group:		Control
@export var Account_Input: 		LineEdit
@export var Password_Input: 	LineEdit

var login_success: 		String = "0"		# 账号成功状态
var login_info_issue: 	String = "1"		# 账号信息问题状态
var login_info_error:	String = "2"		# 账号无误,验证错误

# 登录提示框大小
var tip_size: Vector2 = Vector2(400, 200)

# 弹出登录提示
func _general_tip(
	python_result: String, 
	is_custom: bool = false, 
	custom_tip: String = "") -> void:
	
		
	# 获取当前状态
	var current_user_state: GlobalEnum.User_State
	current_user_state = Login_Group.get_user_state()

	# 弹出提示
	var login_tip = AcceptDialog.new()
	login_tip.title = "登录提示"
	login_tip.size = tip_size
	
	# 自定义提示
	if is_custom:
		# 加入自定义信息
		login_tip.dialog_text = custom_tip	
					
		# 将登录提示加入场景并居中
		get_tree().current_scene.add_child(login_tip)
		login_tip.popup_centered()
		return
	
	# 匹配弹出类型
	match current_user_state:
		# 登录状态
		GlobalEnum.User_State.LOGIN:
			# 匹配登录状态
			match python_result:
				login_success:
					login_tip.dialog_text = "登录成功"
				login_info_issue:
					login_tip.dialog_text = "账号信息不存在"
				login_info_error:
					login_tip.dialog_text = "密码错误"
		# 注册状态
		GlobalEnum.User_State.REGISTER:
			# 匹配注册状态
			match python_result:
				login_success:
					login_tip.dialog_text = "注册成功"
				login_info_issue:
					login_tip.dialog_text = "注册密码非法或长度小于4(账号长度不能小于3)"
				login_info_error:
					login_tip.dialog_text = "注册信息已存在"
	
	# 将登录提示加入场景并居中
	get_tree().current_scene.add_child(login_tip)
	login_tip.popup_centered()

# 登录按钮被点击，传输登录数据
func _on_login_pressed() -> void:
	
	# 获取当前状态
	var current_user_state: GlobalEnum.User_State
	current_user_state = Login_Group.get_user_state()
	
	# 获得输入信息
	var input_account_name: 	String 		= Account_Input.text.strip_edges()
	var input_account_password: String 		= Password_Input.text.strip_edges()
	
	if input_account_name.is_empty() or input_account_password.is_empty():
		_general_tip("0", true, "账号或密码不能为空")
		Password_Input.clear()
		return
		
	var verify_result
	# 匹配用户状态
	match current_user_state:
		GlobalEnum.User_State.LOGIN:
			verify_result = LoginSystem.login_verify(input_account_name, input_account_password)
		GlobalEnum.User_State.REGISTER:
			verify_result = LoginSystem.register_verify(input_account_name, input_account_password)
	
	# 输出提示
	_general_tip(verify_result)
	# 清除密码框
	Password_Input.clear()
			
			
			
			
			
