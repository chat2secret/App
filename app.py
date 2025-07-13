from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # جایگزین کن با یه کلید امن

# ذخیره پیام‌ها
messages = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username in ["user1", "user2"]:
            session["username"] = username
            return redirect(url_for("chat"))
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>ورود به چت</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Tahoma, sans-serif;
            direction: rtl;
            background: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 300px;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        .btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px;
            width: 100%;
        }
        .btn:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>چت خصوصی ✨</h1>
        <p>لطفا انتخاب کن کی هستی:</p>
        <form method="POST">
            <button type="submit" name="username" value="user1" class="btn">من (کاربر ۱)</button>
            <button type="submit" name="username" value="user2" class="btn">دوستم (کاربر ۲)</button>
        </form>
    </div>
</body>
</html>
    ''')

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "username" not in session:
        return redirect(url_for("login"))
    
    current_user = session["username"]
    
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            messages.append({"user": current_user, "text": message})
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>چت دو نفره</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            direction: rtl;
            background: #f0f2f5;
            margin: 0;
            padding: 0;
        }
        .chat-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 10px 10px 0 0;
            text-align: center;
            font-size: 20px;
        }
        .chat-box {
            flex: 1;
            background: white;
            padding: 20px;
            overflow-y: auto;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .message {
            margin-bottom: 15px;
            max-width: 70%;
            padding: 10px 15px;
            border-radius: 18px;
            position: relative;
            word-wrap: break-word;
        }
        .user1 {
            background: #e3f2fd;
            margin-left: auto;
            text-align: right;
            border-bottom-right-radius: 5px;
        }
        .user2 {
            background: #fff8e1;
            margin-right: auto;
            text-align: left;
            border-bottom-left-radius: 5px;
        }
        .message-form {
            display: flex;
            margin-top: 15px;
        }
        .message-input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
        }
        .send-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 0 25px;
            margin-right: 10px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
        }
        .send-btn:hover {
            background: #45a049;
        }
        .user-label {
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            💬 چت خصوصی | شما به عنوان {{ "من" if session["username"] == "user1" else "دوستم" }} هستید
        </div>
        
        <div class="chat-box">
            {% for msg in messages %}
                <div class="message {{ 'user1' if msg.user == 'user1' else 'user2' }}">
                    <span class="user-label">{{ 'من' if msg.user == 'user1' else 'دوستم' }}</span>
                    {{ msg.text }}
                </div>
            {% endfor %}
        </div>
        
        <form method="POST" class="message-form">
            <input type="text" name="message" class="message-input" placeholder="پیامتو بنویس..." required>
            <button type="submit" class="send-btn">ارسال</button>
        </form>
    </div>
</body>
</html>
    ''', messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
