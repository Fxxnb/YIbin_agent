class ConversationBuffer:
    def __init__(self):
        self.messages = []  # [{"role": "user", "content": "..."}, ...]

    def add_user_message(self, text: str):
        self.messages.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str):
        self.messages.append({"role": "assistant", "content": text})

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []