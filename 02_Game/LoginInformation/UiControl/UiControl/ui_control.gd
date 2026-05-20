extends Control

# 退出登录
func _on_exit_login_pressed() -> void:
	await get_tree().create_timer(1.0).timeout

	LoginSystem.exit_login()
	get_tree().change_scene_to_file("res://02_Game/Level/GameUsingLevel/game_using_level.tscn")
