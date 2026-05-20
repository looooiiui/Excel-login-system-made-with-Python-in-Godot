extends Label

func _physics_process(delta: float) -> void:
	detected_login_state()

# 检查登录状态，更新信息
func detected_login_state() -> void:
	if text != "登录ID: " + LoginSystem.get_current_id():
		text = "登录ID: " + LoginSystem.get_current_id()
	return
