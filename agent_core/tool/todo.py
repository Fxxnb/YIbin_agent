todo_list = []


def add_todo(item: str) -> str:
    if not item:
        return "待办内容不能为空。"
    todo_list.append(item)
    return f"已添加：{item}"


def list_todo() -> str:
    if not todo_list:
        return "暂无待办事项。"
    result = "\n".join([f"{index + 1}. {item}" for index, item in enumerate(todo_list)])
    return f"你的待办：\n{result}"


def delete_todo(index: int) -> str:
    if 1 <= index <= len(todo_list):
        removed = todo_list.pop(index - 1)
        return f"已删除编号 {index} 的待办：{removed}"
    return f"编号 {index} 无效，请检查。"
