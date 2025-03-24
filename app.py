from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
from ai_model import AIHelpDesk  # AI modelini import ediyoruz

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

# AI model instance'ı oluştur
ai_helpdesk = AIHelpDesk()

# Veritabanı Modelleri
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    company_name = db.Column(db.String(100))
    department = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    position = db.Column(db.String(50))
    tickets = db.relationship('Ticket', back_populates='user', lazy=True)
    responses = db.relationship('TicketResponse', back_populates='user', lazy=True)
    status_changes = db.relationship('TicketStatusHistory', back_populates='changed_by', lazy=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')
    priority = db.Column(db.String(20), default='low')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='tickets')
    responses = db.relationship('TicketResponse', back_populates='ticket', lazy=True)
    status_history = db.relationship('TicketStatusHistory', back_populates='ticket', lazy=True)

class TicketResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket = db.relationship('Ticket', back_populates='responses')
    user = db.relationship('User', back_populates='responses')

class TicketStatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    old_status = db.Column(db.String(20))
    new_status = db.Column(db.String(20), nullable=False)
    changed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.Text)
    ticket = db.relationship('Ticket', back_populates='status_history')
    changed_by = db.relationship('User', back_populates='status_changes')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tickets = db.relationship('Ticket', backref='category', lazy=True)
    
    @property
    def ticket_count(self):
        return len(self.tickets)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

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

# Kullanıcı kaydı
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        company_name = request.form.get('company_name')
        department = request.form.get('department')
        phone = request.form.get('phone')
        position = request.form.get('position')
        
        # Kullanıcı adı veya email zaten kullanılıyor mu kontrol et
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('Bu kullanıcı adı veya email zaten kullanılıyor')
            return render_template('register.html')
        
        # Yeni kullanıcı oluştur
        new_user = User(
            username=username,
            password=password,  # Gerçek uygulamada şifre hash'lenmelidir
            email=email,
            company_name=company_name,
            department=department,
            phone=phone,
            position=position,
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

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
        # Admin tüm ticketları görebilir
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        # Normal kullanıcı sadece kendi ticketlarını görebilir
        tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    
    open_tickets = Ticket.query.filter_by(status='open').count()
    resolved_tickets = Ticket.query.filter_by(status='resolved').count()
    pending_tickets = Ticket.query.filter_by(status='in_progress').count()
    
    return render_template('dashboard.html', 
                         tickets=tickets,
                         open_tickets=open_tickets,
                         resolved_tickets=resolved_tickets,
                         pending_tickets=pending_tickets)

# Yeni ticket oluşturma
@app.route('/ticket/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    if request.method == 'POST':
        description = request.form.get('description')
        
        # AI ile kategori önerisi al
        suggested_category = ai_helpdesk.suggest_category(description)
        
        ticket = Ticket(
            title=request.form.get('title'),
            description=description,
            priority=request.form.get('priority'),
            category_id=suggested_category,  # Önerilen kategoriyi kullan
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        
        # Otomatik yanıt önerisi al
        auto_response = ai_helpdesk.get_auto_response(description)
        if auto_response['confidence'] > 0.8:  # Güven skoru yüksekse
            response = TicketResponse(
                content=auto_response['response'],
                ticket_id=ticket.id,
                user_id=1  # Admin kullanıcı ID'si
            )
            db.session.add(response)
            db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    categories = ['Teknik Destek', 'Yazılım', 'Donanım', 'Ağ', 'Diğer']
    return render_template('new_ticket.html', categories=categories)

# Ticket detayı
@app.route('/ticket/<int:ticket_id>')
@login_required
def ticket_detail(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)
    if not ticket:
        flash('Ticket bulunamadı.')
        return redirect(url_for('dashboard'))
    
    # Kullanıcı yetkisi kontrolü
    if not current_user.is_admin and ticket.user_id != current_user.id:
        flash('Bu ticketı görüntüleme yetkiniz yok.')
        return redirect(url_for('dashboard'))
    
    statuses = ['Açık', 'İşlemde', 'Beklemede', 'Çözüldü', 'Kapalı']
    return render_template('ticket_detail.html', 
                         ticket=ticket, 
                         is_admin=current_user.is_admin,
                         statuses=statuses)

# Ticket yanıtı ekleme
@app.route('/ticket/<int:ticket_id>/response', methods=['POST'])
@login_required
def add_response(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Kullanıcı yetkisi kontrolü
    if not current_user.is_admin and ticket.user_id != current_user.id:
        flash('Bu ticketa yanıt ekleme yetkiniz yok.')
        return redirect(url_for('ticket_detail', ticket_id=ticket_id))
    
    response_content = request.form.get('content')
    
    response = TicketResponse(
        content=response_content,
        ticket_id=ticket_id,
        user_id=current_user.id
    )
    db.session.add(response)
    db.session.commit()
    
    # Ticket çözüldüyse bilgi tabanını güncelle
    if ticket.status == 'Çözüldü':
        ai_helpdesk.update_knowledge_base(ticket)
    
    return redirect(url_for('ticket_detail', ticket_id=ticket_id))

# Ticket durumu güncelleme
@app.route('/ticket/<int:ticket_id>/status', methods=['POST'])
@login_required
def update_ticket_status(ticket_id):
    if not current_user.is_admin:
        flash('Yalnızca yöneticiler ticket durumunu değiştirebilir.')
        return redirect(url_for('ticket_detail', ticket_id=ticket_id))
    
    ticket = db.session.get(Ticket, ticket_id)
    if not ticket:
        flash('Ticket bulunamadı.')
        return redirect(url_for('dashboard'))
    
    new_status = request.form.get('status')
    note = request.form.get('note', '')
    
    if new_status and new_status != ticket.status:
        # Durum değişikliğini kaydet
        history = TicketStatusHistory(
            ticket_id=ticket.id,
            old_status=ticket.status,
            new_status=new_status,
            changed_by_id=current_user.id,
            note=note
        )
        ticket.status = new_status
        db.session.add(history)
        db.session.commit()
        
        flash(f'Ticket durumu güncellendi: {new_status}')
    
    return redirect(url_for('ticket_detail', ticket_id=ticket_id))

# AI önerilerini almak için API endpoint'i
@app.route('/api/ai/suggest', methods=['POST'])
@login_required
def ai_suggestions():
    text = request.json.get('text', '')
    
    suggestions = {
        'category': ai_helpdesk.suggest_category(text),
        'auto_response': ai_helpdesk.get_auto_response(text)
    }
    
    return jsonify(suggestions)

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

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    # İstatistikler
    total_tickets = Ticket.query.count()
    resolved_tickets = Ticket.query.filter_by(status='resolved').count()
    pending_tickets = Ticket.query.filter_by(status='pending').count()
    urgent_tickets = Ticket.query.filter_by(priority='high').count()
    
    # Kullanıcılar
    users = User.query.order_by(User.created_at.desc()).all()
    
    # Ticketlar
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    
    # Kategoriler
    categories = Category.query.all()
    
    return render_template('admin.html',
                         total_tickets=total_tickets,
                         resolved_tickets=resolved_tickets,
                         pending_tickets=pending_tickets,
                         urgent_tickets=urgent_tickets,
                         users=users,
                         tickets=tickets,
                         categories=categories)

@app.route('/api/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'company_name': user.company_name,
        'department': user.department,
        'phone': user.phone,
        'position': user.position
    })

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.company_name = data.get('company_name', user.company_name)
    user.department = data.get('department', user.department)
    user.phone = data.get('phone', user.phone)
    user.position = data.get('position', user.position)
    user.is_admin = data.get('role') == 'admin'
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
@login_required
def get_ticket(ticket_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    ticket = Ticket.query.get_or_404(ticket_id)
    return jsonify({
        'id': ticket.id,
        'title': ticket.title,
        'category_id': ticket.category_id,
        'priority': ticket.priority,
        'status': ticket.status
    })

@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
@login_required
def update_ticket(ticket_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    ticket = Ticket.query.get_or_404(ticket_id)
    data = request.get_json()
    
    ticket.title = data.get('title', ticket.title)
    ticket.category_id = data.get('category_id', ticket.category_id)
    ticket.priority = data.get('priority', ticket.priority)
    ticket.status = data.get('status', ticket.status)
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
@login_required
def delete_ticket(ticket_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/categories/<int:category_id>', methods=['GET'])
@login_required
def get_category(category_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    category = Category.query.get_or_404(category_id)
    return jsonify({
        'id': category.id,
        'name': category.name
    })

@app.route('/api/categories/<int:category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    
    category.name = data.get('name', category.name)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/add_category', methods=['POST'])
@login_required
def add_category():
    if not current_user.is_admin:
        flash('Bu işlem için yetkiniz yok.', 'danger')
        return redirect(url_for('admin_panel'))
    
    category_name = request.form.get('category_name')
    if category_name:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()
        flash('Kategori başarıyla eklendi.', 'success')
    else:
        flash('Kategori adı boş olamaz.', 'danger')
    
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(debug=True, host='0.0.0.0', port=5000)
