from agent_core.agent import MyAgent


def main():
    agent = MyAgent()
    print("你的专属 Agent 已启动")
    print("命令：计算 1+2 | 记住 买牛奶 | 我的待办 | 删除待办 1 | 获取当前时间 | 获取宜宾天气 | 获取空气质量 | clear | exit")

    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue
        response = agent.run(user_input)
        print(f"Agent: {response}")


if __name__ == "__main__":
    main()
