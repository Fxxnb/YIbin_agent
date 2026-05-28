from flask import Flask, request, jsonify, render_template_string
from agent_core.agent import MyAgent
import os

app = Flask(__name__)
agent = MyAgent()

# ===== 网页界面 =====
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>My Agent</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 40px auto; }
        #chat { border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: auto; }
        input { width: 80%; padding: 10px; }
        button { padding: 10px; }
        .msg { margin: 8px 0; }
        .user { color: blue; }
        .bot { color: green; }
        .hint { color: gray; font-size: 12px; }
    </style>
</head>
<body>

<h2>🤖 My Agent Chat</h2>

<div class="hint">
支持命令：计算 / 记住 / 待办 / 删除待办 / 当前时间 / 天气 / 空气质量 / clear / exit
</div>

<div id="chat"></div>

<input id="input" placeholder="输入你的问题..." />
<button onclick="sendMsg()">发送</button>

<script>
async function sendMsg() {
    let input = document.getElementById("input");
    let msg = input.value;
    if (!msg) return;

    document.getElementById("chat").innerHTML +=
        "<div class='msg user'>你: " + msg + "</div>";

    input.value = "";

    let res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg})
    });

    let data = await res.json();

    document.getElementById("chat").innerHTML +=
        "<div class='msg bot'>Agent: " + data.response + "</div>";

    document.getElementById("chat").scrollTop = 999999;
}
</script>

</body>
</html>
"""

# ===== 首页 =====
@app.route("/")
def home():
    return render_template_string(HTML)

# ===== 聊天接口（核心）=====
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "请输入内容"})

    try:
        # 直接调用你原来的 Agent
        response = agent.run(user_input)
    except Exception as e:
        response = f"运行出错：{str(e)}"

    return jsonify({"response": response})

# ===== 健康检查 =====
@app.route("/health")
def health():
    return "ok"

# ===== Railway启动 =====
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
