from flask import Flask, request, jsonify
from agent_core.agent import MyAgent

app = Flask(__name__)

agent = MyAgent()

@app.route("/")
def home():
    return "My Agent is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "请输入内容"})

    response = agent.run(user_input)

    return jsonify({
        "response": response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
