from flask import Flask, request, render_template_string

app = Flask(__name__)

# ذخیره پیام‌ها (در حالت واقعی از دیتابیس استفاده کن)
messages = []

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("message")
        
        if username and message:
            messages.append({"user": username, "text": message})
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>چت دو نفره</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Tahoma, sans-serif;
            direction: rtl;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .chat-box {
            border: 1px solid #ddd;
            padding: 10px;
            height: 400px;
            overflow-y: auto;
            margin-bottom: 10px;
            background: #f9f9f9;
        }
        .message {
            margin: 5px 0;
            padding: 8px;
            border-radius: 5px;
        }
        .user1 {
            background: #e3f2fd;
            text-align: right;
        }
        .user2 {
            background: #fff8e1;
            text-align: left;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        input, button {
            padding: 8px;
            margin: 5px 0;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>چت خصوصی (من و دوستم) 💬</h1>
    
    <div class="chat-box">
        {% for msg in messages %}
            <div class="message {{ 'user1' if msg.user == 'user1' else 'user2' }}">
                <strong>{{ 'من' if msg.user == 'user1' else 'دوستم' }}:</strong> {{ msg.text }}
            </div>
        {% endfor %}
    </div>
    
    <form method="POST">
        <select name="username" required>
            <option value="">-- انتخاب کاربر --</option>
            <option value="user1">من (کاربر ۱)</option>
            <option value="user2">دوستم (کاربر ۲)</option>
        </select>
        <input type="text" name="message" placeholder="پیامتو بنویس..." required>
        <button type="submit">ارسال</button>
    </form>
</body>
</html>
    ''', messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
