from flask import Flask, request, jsonify, session, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template
from io import BytesIO
from PIL import Image
from flask import send_file
from utils import generate_captcha

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
str_val = ""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) and len(password) >= 6
    
with app.app_context():
    db.create_all()

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 检查表单是否包含 'username' 和 'password' 字段
        if 'username' not in request.form or 'password' not in request.form:
            # 如果字段缺失，使用 flash 显示错误消息，并重定向回登录页面
            flash('Please provide both username and password', 'error')
            return redirect(url_for('login_page'))
        
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = username
            # flash('Logged in successfully !')
            return  redirect(url_for('collect_analyze_page'))   
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login_page'))
    else:
        # 如果是 GET 请求，显示登录表单
        return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 从表单中获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        captcha = request.form.get('captcha')
        # 检查验证码
        if not validate_captcha(captcha):
            flash('Invalid captcha', 'error')
            return redirect(url_for('register_page'))

        # 检查密码是否匹配
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register_page'))

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('register_page'))

        # 创建新用户
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registered successfully', 'success')
        return redirect(url_for('login_page'))
    else:
        # GET 请求，显示注册表单
        return render_template('register.html')

@app.route('/captcha')
def captcha():
    global str_val
    file_path,str_val = generate_captcha()
    with Image.open(file_path) as img:
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')

def validate_captcha(captcha_input):
    # 这里应该是验证验证码的逻辑
    # 这只是一个示例，你需要实现具体的验证码验证逻辑
    global str_val
    return captcha_input == str_val

@app.route('/collect-analyze')
def collect_analyze_page():
    if 'user_id' not in session:  # 检查用户是否登录
        return redirect(url_for('login_page'))  # 如果没有登录，重定向到登录页面
    return render_template('collect_analyze.html')  # 渲染包含数据采集和分析按钮的页面

@app.route('/collect', methods=['POST'])
def collect_data():
    if 'user_id' not in session:  # 检查用户是否登录
        return jsonify({'error': 'You must be logged in to collect data.'})
    data = request.json
    # 存储数据逻辑
    # ...
    return jsonify({'message': 'Data collected'})

@app.route('/analyze', methods=['POST'])
def analyze_data():
    if 'user_id' not in session:  # 检查用户是否登录
        return jsonify({'error': 'You must be logged in to analyze data.'})
    def mock_ai_analysis(data):
        # 这里应该是机器学习模型的分析逻辑
        return {'result': 'analysis of ' + str(data)}
    
    data = request.json
    result = mock_ai_analysis(data)
    return jsonify(result)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.route('/')
def index():
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run()