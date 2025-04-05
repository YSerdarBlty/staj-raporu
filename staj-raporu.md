# Staj Raporu

## 1. Gün (18.03.2024)
### Yapılan İşler
1. Proje Tanıtımı ve Kurulum
   - Flask framework'ü hakkında bilgi edinildi
   - Proje yapısı oluşturuldu
   - Gerekli kütüphaneler yüklendi (Flask, SQLAlchemy, Flask-Login)
   - Veritabanı şeması tasarlandı

### Öğrenilen Konular
- Flask framework'ün temel yapısı
- SQLAlchemy ORM kullanımı
- Veritabanı modelleme
- Proje yapılandırması

### Kod Örnekleri
```python
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Veritabanı modelleri
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
```

## 2. Gün (19.03.2024)
### Yapılan İşler
1. Kullanıcı Yönetimi
   - Kullanıcı modeli oluşturuldu
   - Kayıt ve giriş sayfaları tasarlandı
   - Şifre hashleme implementasyonu yapıldı
   - Kullanıcı yetkilendirme sistemi kuruldu

### Öğrenilen Konular
- Flask-Login kullanımı
- Şifre güvenliği
- Session yönetimi
- Form validasyonu

### Kod Örnekleri
```python
# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Geçersiz kullanıcı adı veya şifre')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten kullanılıyor')
            return redirect(url_for('auth.register'))
            
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')
```

## 3. Gün (20.03.2024)
### Yapılan İşler
1. Ticket Sistemi
   - Ticket modeli oluşturuldu
   - Ticket oluşturma formu tasarlandı
   - Ticket listeleme sayfası yapıldı
   - Kategori ve öncelik sistemi eklendi

### Öğrenilen Konular
- Form işleme
- Veritabanı ilişkileri
- Template inheritance
- Bootstrap kullanımı

### Kod Örnekleri
```python
# models.py
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')
    priority = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    user = db.relationship('User', backref='tickets')
    category = db.relationship('Category', backref='tickets')
    responses = db.relationship('TicketResponse', backref='ticket', cascade='all, delete-orphan')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
```

## 4. Gün (21.03.2024)
### Yapılan İşler
1. Ticket Detay Sayfası
   - Ticket detay görünümü oluşturuldu
   - Yanıt sistemi implementasyonu yapıldı
   - Durum güncelleme özelliği eklendi
   - Dosya yükleme özelliği eklendi

### Öğrenilen Konular
- File upload işlemleri
- AJAX kullanımı
- Dynamic form handling
- Bootstrap modal kullanımı

### Kod Örnekleri
```python
# routes.py
@app.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
        response = TicketResponse(
            content=request.form.get('content'),
            ticket_id=ticket_id,
            user_id=current_user.id
        )
        db.session.add(response)
        db.session.commit()
        flash('Yanıtınız başarıyla eklendi')
        return redirect(url_for('ticket_detail', ticket_id=ticket_id))
        
    return render_template('ticket_detail.html', ticket=ticket)
```

## 5. Gün (22.03.2024)
### Yapılan İşler
1. Admin Paneli
   - Admin dashboard tasarlandı
   - Kullanıcı yönetimi eklendi
   - Ticket yönetimi eklendi
   - İstatistik sayfası oluşturuldu

### Öğrenilen Konular
- Admin yetkilendirme
- Dashboard tasarımı
- Veri görselleştirme
- Chart.js kullanımı

### Kod Örnekleri
```python
# admin.py
@admin.route('/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok')
        return redirect(url_for('main.dashboard'))
        
    total_tickets = Ticket.query.count()
    open_tickets = Ticket.query.filter_by(status='open').count()
    resolved_tickets = Ticket.query.filter_by(status='resolved').count()
    total_users = User.query.count()
    
    return render_template('admin/dashboard.html',
                         total_tickets=total_tickets,
                         open_tickets=open_tickets,
                         resolved_tickets=resolved_tickets,
                         total_users=total_users)
```

## 6. Gün (25.03.2024)
### Yapılan İşler
1. Güvenlik İyileştirmeleri
   - CSRF koruması eklendi
   - XSS koruması eklendi
   - SQL injection koruması eklendi
   - Rate limiting implementasyonu yapıldı

### Öğrenilen Konular
- Web güvenliği
- Güvenlik açıkları
- Koruma yöntemleri
- Flask-Security kullanımı

### Kod Örnekleri
```python
# security.py
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_request
def before_request():
    if request.method == 'POST':
        if not request.form.get('csrf_token'):
            abort(403)
            
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

## 7. Gün (26.03.2024)
### Yapılan İşler
1. Ticket Yönetimi İyileştirmeleri
   - Ticket silme özelliği eklendi
   - Yanıt silme özelliği eklendi
   - Durum güncelleme formu düzenlendi
   - Not ekleme özelliği eklendi

### Öğrenilen Konular
- Cascade delete işlemleri
- Form validasyonu
- Flash mesajları
- Bootstrap 5 özellikleri

### Kod Örnekleri
```python
# routes.py
@app.route('/ticket/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if not current_user.is_admin and ticket.user_id != current_user.id:
        flash('Bu işlem için yetkiniz yok')
        return redirect(url_for('ticket_detail', ticket_id=ticket_id))
        
    try:
        db.session.delete(ticket)
        db.session.commit()
        flash('Ticket başarıyla silindi')
    except Exception as e:
        db.session.rollback()
        flash('Ticket silinirken bir hata oluştu')
        
    return redirect(url_for('dashboard'))
```

## 8. Gün (27.03.2024)
### Yapılan İşler
1. Kullanıcı Arayüzü Geliştirmeleri
   - Responsive tasarım iyileştirmeleri
   - Kullanıcı dostu hata mesajları
   - Loading animasyonları
   - Dark mode desteği

### Öğrenilen Konular
- CSS3 özellikleri
- JavaScript animasyonları
- Responsive design
- Bootstrap 5 grid sistemi

### Kod Örnekleri
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %} - Help Desk</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        .loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 9999;
        }
        .loading-spinner {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
    </style>
</head>
<body>
    {% include 'navbar.html' %}
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
    <div class="loading">
        <div class="loading-spinner">
            <div class="spinner-border text-light" role="status">
                <span class="visually-hidden">Yükleniyor...</span>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const loading = document.querySelector('.loading');
            document.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', () => {
                    loading.style.display = 'block';
                });
            });
        });
    </script>
</body>
</html>
```

## 9. Gün (28.03.2024)
### Yapılan İşler
1. Veritabanı Optimizasyonu
   - İndeksler eklendi
   - Query optimizasyonu yapıldı
   - Caching mekanizması eklendi
   - Connection pooling yapılandırıldı

### Öğrenilen Konular
- SQL optimizasyonu
- Database indexing
- Caching stratejileri
- Connection management

### Kod Örnekleri
```python
# models.py
class Ticket(db.Model):
    __tablename__ = 'tickets'
    __table_args__ = (
        db.Index('idx_ticket_status', 'status'),
        db.Index('idx_ticket_priority', 'priority'),
        db.Index('idx_ticket_user', 'user_id'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')
    priority = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    @classmethod
    def get_user_tickets(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc())
```

## 10. Gün (29.03.2024)
### Yapılan İşler
1. API Geliştirme
   - RESTful API endpoints oluşturuldu
   - API dokümantasyonu yazıldı
   - API authentication eklendi
   - Rate limiting implementasyonu

### Öğrenilen Konular
- REST API tasarımı
- API authentication
- API documentation
- Flask-RESTful kullanımı

### Kod Örnekleri
```python
# api.py
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Api(app)

class TicketResource(Resource):
    @jwt_required()
    def get(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        return {
            'id': ticket.id,
            'title': ticket.title,
            'description': ticket.description,
            'status': ticket.status,
            'created_at': ticket.created_at.isoformat()
        }
    
    @jwt_required()
    def put(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.get_json()
        
        if 'status' in data:
            ticket.status = data['status']
        if 'priority' in data:
            ticket.priority = data['priority']
            
        db.session.commit()
        return {'message': 'Ticket güncellendi'}

api.add_resource(TicketResource, '/api/tickets/<int:ticket_id>')
```

## 11. Gün (01.04.2024)
### Yapılan İşler
1. Test Geliştirme
   - Unit testler yazıldı
   - Integration testler eklendi
   - Test coverage raporu oluşturuldu
   - CI/CD pipeline kuruldu

### Öğrenilen Konular
- Python unittest
- Test coverage
- CI/CD pipeline
- GitHub Actions

### Kod Örnekleri
```python
# tests/test_ticket.py
import unittest
from app import create_app, db
from app.models import User, Ticket

class TicketTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_create_ticket(self):
        user = User(username='test', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        ticket = Ticket(
            title='Test Ticket',
            description='Test Description',
            user_id=user.id
        )
        db.session.add(ticket)
        db.session.commit()
        
        self.assertEqual(Ticket.query.count(), 1)
        self.assertEqual(ticket.title, 'Test Ticket')
```

## 12. Gün (02.04.2024)
### Yapılan İşler
1. Performans İyileştirmeleri
   - Lazy loading implementasyonu
   - Asset optimizasyonu
   - Database query optimizasyonu
   - Caching stratejileri

### Öğrenilen Konular
- Performance optimization
- Lazy loading
- Asset management
- Caching techniques

### Kod Örnekleri
```python
# cache.py
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@app.route('/dashboard')
@cache.cached(timeout=300)
@login_required
def dashboard():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tickets=tickets)

# Lazy loading için JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                observer.unobserve(img);
            }
        });
    });
    images.forEach(img => imageObserver.observe(img));
});
```

## 13. Gün (03.04.2024)
### Yapılan İşler
1. Bildirim Sistemi
   - Email bildirimleri eklendi
   - In-app bildirimler eklendi
   - Web push notifications
   - Bildirim tercihleri

### Öğrenilen Konular
- Email sending
- Web push notifications
- Real-time updates
- User preferences

### Kod Örnekleri
```python
# notifications.py
from flask_mail import Message
from flask import current_app
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

@app.route('/notifications/subscribe', methods=['POST'])
@login_required
def subscribe_notifications():
    subscription = request.get_json()
    current_user.push_subscription = json.dumps(subscription)
    db.session.commit()
    return jsonify({'status': 'success'})

# Service Worker
self.addEventListener('push', function(event) {
    const data = event.data.json();
    self.registration.showNotification(data.title, {
        body: data.body,
        icon: '/static/icon.png'
    });
});
```

## 14. Gün (04.04.2024)
### Yapılan İşler
1. Raporlama Modülü
   - Ticket istatistikleri
   - Kullanıcı aktivite raporları
   - PDF export özelliği
   - Excel export özelliği

### Öğrenilen Konular
- Data visualization
- PDF generation
- Excel export
- Report generation

### Kod Örnekleri
```python
# reports.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import pandas as pd

def generate_ticket_report(tickets, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    
    data = [['ID', 'Başlık', 'Durum', 'Öncelik', 'Oluşturulma Tarihi']]
    for ticket in tickets:
        data.append([
            ticket.id,
            ticket.title,
            ticket.status,
            ticket.priority,
            ticket.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
```

## 15. Gün (05.04.2024)
### Yapılan İşler
1. AI Destekli Özellikler
   - Otomatik kategori önerisi
   - Benzer ticket önerileri
   - Otomatik yanıt önerileri
   - Ticket önceliklendirme

### Öğrenilen Konular
- Machine learning
- Natural language processing
- AI integration
- Recommendation systems

### Kod Örnekleri
```python
# ai_model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TicketClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.tickets = []
        self.categories = []
        
    def train(self, tickets, categories):
        self.tickets = tickets
        self.categories = categories
        self.vectorizer.fit([ticket.description for ticket in tickets])
        
    def predict_category(self, description):
        if not self.tickets:
            return None
            
        new_vector = self.vectorizer.transform([description])
        ticket_vectors = self.vectorizer.transform([ticket.description for ticket in self.tickets])
        
        similarities = cosine_similarity(new_vector, ticket_vectors)[0]
        most_similar_idx = np.argmax(similarities)
        
        return self.tickets[most_similar_idx].category
```

## 16. Gün (08.04.2024)
### Yapılan İşler
1. Çoklu Dil Desteği
   - i18n implementasyonu
   - Dil dosyaları oluşturuldu
   - Dil değiştirme özelliği
   - RTL desteği

### Öğrenilen Konular
- Internationalization
- Localization
- RTL support
- Language switching

### Kod Örnekleri
```python
# babel.py
from flask_babel import Babel, gettext as _

babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['tr', 'en'])

# Dil dosyası (messages.po)
msgid "Ticket"
msgstr "Destek Talebi"

msgid "Status"
msgstr "Durum"

msgid "Priority"
msgstr "Öncelik"

# Template kullanımı
<h1>{{ _('Ticket Details') }}</h1>
<p>{{ _('Status') }}: {{ ticket.status }}</p>
<p>{{ _('Priority') }}: {{ ticket.priority }}</p>
```

## 17. Gün (09.04.2024)
### Yapılan İşler
1. Backup ve Recovery
   - Otomatik yedekleme sistemi
   - Veritabanı yedekleme
   - Dosya yedekleme
   - Recovery prosedürleri

### Öğrenilen Konular
- Backup strategies
- Database backup
- File backup
- Disaster recovery

### Kod Örnekleri
```python
# backup.py
import subprocess
from datetime import datetime
import os

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(app.config['BACKUP_FOLDER'], 'database')
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_file = os.path.join(backup_dir, f'backup_{timestamp}.sql')
    
    # SQLite backup
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        subprocess.run(['sqlite3', db_path, f'.backup {backup_file}'])
    
    # MySQL backup
    elif app.config['SQLALCHEMY_DATABASE_URI'].startswith('mysql'):
        subprocess.run([
            'mysqldump',
            '-u', app.config['MYSQL_USER'],
            '-p' + app.config['MYSQL_PASSWORD'],
            app.config['MYSQL_DATABASE'],
            '>', backup_file
        ])
    
    return backup_file
```

## 18. Gün (10.04.2024)
### Yapılan İşler
1. Monitoring ve Logging
   - Error logging sistemi
   - Performance monitoring
   - User activity logging
   - Log analizi

### Öğrenilen Konular
- Logging systems
- Monitoring tools
- Error tracking
- Performance analysis

### Kod Örnekleri
```python
# logging.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
        
    file_handler = RotatingFileHandler('logs/helpdesk.log',
                                     maxBytes=10240,
                                     backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Help Desk startup')

# Performance monitoring
@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    app.logger.info(f'Request took {diff} seconds')
    return response
```

## 19. Gün (11.04.2024)
### Yapılan İşler
1. Deployment ve DevOps
   - Docker containerization
   - Kubernetes deployment
   - CI/CD pipeline
   - Environment configuration

### Öğrenilen Konular
- Docker
- Kubernetes
- DevOps practices
- Deployment strategies

### Kod Örnekleri
```yaml
# docker-compose.yml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/helpdesk
    depends_on:
      - db
    volumes:
      - .:/app
      - uploads:/app/uploads
      
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=helpdesk
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
volumes:
  postgres_data:
  uploads:
```

## 20. Gün (12.04.2024)
### Yapılan İşler
1. Final Test ve Dokümantasyon
   - Son testler yapıldı
   - Kullanıcı kılavuzu yazıldı
   - API dokümantasyonu güncellendi
   - Deployment kılavuzu hazırlandı

### Öğrenilen Konular
- Documentation
- Testing strategies
- User guides
- Technical writing

### Kod Örnekleri
```python
# docs.py
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Help Desk API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Swagger JSON
{
    "swagger": "2.0",
    "info": {
        "title": "Help Desk API",
        "description": "API documentation for Help Desk application",
        "version": "1.0.0"
    },
    "paths": {
        "/api/tickets": {
            "get": {
                "summary": "Get all tickets",
                "responses": {
                    "200": {
                        "description": "List of tickets"
                    }
                }
            }
        }
    }
}
``` 