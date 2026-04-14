import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# তোমার কনফিগারেশন
HF_API_TOKEN = "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"
CHAT_API_URL = "https://router.huggingface.co/v1/chat/completions"
CHAT_MODEL = "deepseek-ai/DeepSeek-V3"

def query_jarvis_ai(prompt):
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    system_prompt = (
        "তুমি JARVIS। সবসময় তোমার উত্তর শুরু করবে 😊 দিয়ে। "
        "সবসময় বাংলায় কথা বলবে। স্ত্রীলিঙ্গে কথা বলবে। "
        "উত্তর খুব সংক্ষিপ্ত রাখবে (১-২ বাক্য)।"
    )

    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(CHAT_API_URL, headers=headers, json=payload, timeout=25)
        result = response.json()
        return result.get('choices', [{}])[0].get('message', {}).get('content', "😊 মাফ করো, আমি এখন কোনো উত্তর দিতে পারছি না।")
    except Exception as e:
        return f"😊 এরর: {str(e)}"

# --- API Endpoints ---

@app.route('/ask', methods=['GET'])
def ask_jarvis():
    # URL থেকে প্রশ্ন নিবে: /ask?query=কেমন আছো?
    user_query = request.args.get('query')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    ai_response = query_jarvis_ai(user_query)
    return jsonify({
        "status": "success",
        "bot_name": "JARVIS",
        "response": ai_response
    })

app = Flask(__name__)

# ... আপনার বাকি সব কোড ...

# ফাইলের একদম শেষে শুধু এই লাইনটি থাকবে (app.run দরকার নেই)
# app.run() বাদ দিন
