from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

app = Flask(__name__, 
    template_folder='templates',  # Şablon dizinini belirtiyoruz
    static_folder='static'        # Statik dosyalar için dizin
)
app.config['SECRET_KEY'] = 'gizli-anahtar-buraya'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
app.config['DEBUG'] = True  # Hata ayıklama modunu aktif ediyoruz
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Veritabanı Modelleri
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    tickets = db.relationship('Ticket', backref='user', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Açık')
    priority = db.Column(db.String(20), default='Normal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    responses = db.relationship('TicketResponse', backref='ticket', lazy=True)

class TicketResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Giriş sayfası
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # Gerçek uygulamada şifre hash'lenmelidir
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Geçersiz kullanıcı adı veya şifre')
    return render_template('login.html')

# Çıkış
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tickets=tickets)

# Yeni ticket oluşturma
@app.route('/ticket/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    if request.method == 'POST':
        ticket = Ticket(
            title=request.form.get('title'),
            description=request.form.get('description'),
            priority=request.form.get('priority'),
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('new_ticket.html')

# Ticket detayı
@app.route('/ticket/<int:ticket_id>')
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not current_user.is_admin and ticket.user_id != current_user.id:
        return redirect(url_for('dashboard'))
    return render_template('ticket_detail.html', ticket=ticket)

# Ticket yanıtı ekleme
@app.route('/ticket/<int:ticket_id>/response', methods=['POST'])
@login_required
def add_response(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not current_user.is_admin and ticket.user_id != current_user.id:
        return redirect(url_for('dashboard'))
    
    response = TicketResponse(
        content=request.form.get('content'),
        ticket_id=ticket_id,
        user_id=current_user.id
    )
    db.session.add(response)
    db.session.commit()
    return redirect(url_for('ticket_detail', ticket_id=ticket_id))

def create_admin_user():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password='admin123',  # Gerçek uygulamada şifre hash'lenmelidir
            email='admin@example.com',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(debug=True, host='0.0.0.0', port=5000)
