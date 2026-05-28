from flask import Flask, request, jsonify, render_template_string
from agent_core.agent import MyAgent
import os

app = Flask(__name__)
agent = MyAgent()

# ===== 极简页面 =====
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Agent</title>
    <style>
        body { font-family: Arial; max-width: 700px; margin: 40px auto; }
        #chat { border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: auto; }
        input { width: 80%; padding: 10px; }
        button { padding: 10px; }
        .user { color: blue; margin: 5px 0; }
        .bot { color: green; margin: 5px 0; }
    </style>
</head>
<body>

<h3>My Agent</h3>

<div id="chat"></div>

<input id="input" placeholder="输入问题..." />
<button onclick="send()">发送</button>

<script>
async function send() {
    let input = document.getElementById("input");
    let msg = input.value;
    if (!msg) return;

    document.getElementById("chat").innerHTML += "<div class='user'>你: " + msg + "</div>";

    input.value = "";

    let res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg})
    });

    let data = await res.json();

    document.getElementById("chat").innerHTML += "<div class='bot'>Agent: " + data.response + "</div>";

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

# ===== 对话接口 =====
@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")

    try:
        reply = agent.run(msg)
    except Exception as e:
        reply = f"错误: {str(e)}"

    return jsonify({"response": reply})

# ===== Railway启动 =====
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
