from agent_core.my_llm.client import LLMClient
from agent_core.memory.memory import ConversationBuffer
from agent_core.tool.calculator import calculate
from agent_core.tool.todo import add_todo, delete_todo, list_todo
from agent_core.tool.tool_time import (
    get_time,
    get_yibin_today_air_quality,
    get_yibin_today_weather,
)


class MyAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.memory = ConversationBuffer()

    def run(self, user_input: str) -> str:
        text = user_input.strip()

        if text.startswith("计算 "):
            expr = text.replace("计算 ", "", 1).strip()
            return calculate(expr)

        if text.startswith("记住 "):
            item = text.replace("记住 ", "", 1).strip()
            return add_todo(item)

        if text in ["我的待办", "列出待办", "待办"]:
            return list_todo()

        if text.startswith("删除待办 "):
            try:
                index = int(text.replace("删除待办 ", "", 1).strip())
                return delete_todo(index)
            except ValueError:
                return "请提供一个数字，例如：删除待办 2"

        if text in ["获取当前时间", "当前时间", "时间"]:
            return get_time()

        if text in ["获取宜宾天气", "宜宾天气", "天气"]:
            return get_yibin_today_weather()

        if text in ["获取空气质量", "宜宾空气质量", "空气质量"]:
            return get_yibin_today_air_quality()

        if text.lower() == "clear":
            self.memory.clear()
            return "对话历史已清除。"

        self.memory.add_user_message(text)
        reply = self.llm.chat(self.memory.get_messages())
        self.memory.add_assistant_message(reply)
        return reply
