# Kırıkkale Üniversitesi Bilgisayar Mühendisliği Staj Raporu

## İçindekiler
1. [Kapak ve Öğrenci Bilgileri](#kapak-ve-öğrenci-bilgileri)
2. [Staj Raporu](#staj-raporu)
3. [Staj Günlüğü](#staj-günlüğü)
4. [Formlar](#formlar)

## Kapak ve Öğrenci Bilgileri

### KIRIKKALE ÜNİVERSİTESİ
#### MÜHENDİSLİK FAKÜLTESİ
##### BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ
###### STAJ DOSYASI

**Öğrenci Bilgileri:**
- Ad Soyad: [Öğrenci Adı Soyadı]
- Öğrenci No: [Öğrenci Numarası]
- Staj Süresi: 20 İş Günü
- Staj Tarihi: [Tarih Aralığı]
- Staj Yeri: [Şirket Adı]
- Staj Türü: İşyeri Stajı

## Staj Raporu

### 1.1. Staj Yapılan Kurum Hakkında Bilgi
- Kurum Adı: [Şirket Adı]
- Kurum Adresi: [Şirket Adresi]
- Kurumun Faaliyet Alanı: Yazılım Geliştirme ve Teknoloji Çözümleri
- Kurumun Web Sitesi: [Web Sitesi]

### 1.2. Staj Süresince Yapılan İşler

#### 1. Gün (Proje Başlangıcı)
**Yapılan İşler:**
- Proje tanımı ve kapsamının belirlenmesi
- Gerekli teknolojilerin seçimi
- Temel özelliklerin belirlenmesi

**Açıklama:**
HelpDesk sistemi için gerekli teknolojiler ve özellikler belirlendi. Modern web teknolojileri kullanılarak kullanıcı dostu bir arayüz tasarlanacak.

**Kullanılan Teknolojiler:**
```python
# Gerekli Python Kütüphaneleri
flask==2.0.1
flask-sqlalchemy==2.5.1
flask-login==0.5.0
```

#### 2. Gün (Veritabanı Tasarımı)
**Yapılan İşler:**
- Veritabanı modellerinin oluşturulması
- İlişkisel veritabanı yapısının tasarlanması

**Açıklama:**
SQLite veritabanı kullanılarak kullanıcılar, ticketlar ve yanıtlar için modeller oluşturuldu.

**Kod Örneği:**
```python
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

#### 3. Gün (Flask Uygulaması Kurulumu)
**Yapılan İşler:**
- Flask framework'ünün kurulumu
- Proje yapısının oluşturulması

**Açıklama:**
Flask uygulaması için temel yapılandırma ve güvenlik ayarları yapıldı.

**Kod Örneği:**
```python
app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)
app.config['SECRET_KEY'] = 'gizli-anahtar-buraya'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
app.config['DEBUG'] = True
```

#### 4. Gün (Kullanıcı Arayüzü Tasarımı - Ana Sayfa)
**Yapılan İşler:**
- Modern ve responsive tasarım
- Bootstrap entegrasyonu

**Açıklama:**
Ana sayfa için modern ve kullanıcı dostu bir arayüz tasarlandı.

**Kod Örneği:**
```html
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HelpDesk - Destek Sistemi</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light fixed-top">
        <!-- Navbar içeriği -->
    </nav>
    <section class="hero-section">
        <!-- Hero section içeriği -->
    </section>
</body>
</html>
```

#### 5. Gün (Giriş Sayfası Tasarımı)
**Yapılan İşler:**
- Kullanıcı girişi formu
- Güvenlik kontrolleri

**Açıklama:**
Güvenli ve kullanıcı dostu bir giriş sayfası tasarlandı.

**Kod Örneği:**
```html
<div class="login-container">
    <div class="login-header">
        <i class="bi bi-headset display-4 mb-3"></i>
        <h2>HelpDesk</h2>
    </div>
    <form method="POST" action="{{ url_for('login') }}">
        <div class="mb-3">
            <input type="text" class="form-control" name="username" required>
        </div>
        <div class="mb-3">
            <input type="password" class="form-control" name="password" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">Giriş Yap</button>
    </form>
</div>
```

#### 6. Gün (Dashboard Sayfası Tasarımı)
**Yapılan İşler:**
- Sidebar menü
- Ticket listesi

**Açıklama:**
Kullanıcıların ticketlarını yönetebileceği dashboard sayfası tasarlandı.

**Kod Örneği:**
```html
<div class="sidebar">
    <div class="sidebar-header">
        <i class="bi bi-headset display-4"></i>
        <h4 class="mt-2">HelpDesk</h4>
    </div>
    <nav class="nav flex-column">
        <a class="nav-link active" href="{{ url_for('dashboard') }}">
            <i class="bi bi-speedometer2"></i> Dashboard
        </a>
        <a class="nav-link" href="{{ url_for('new_ticket') }}">
            <i class="bi bi-plus-circle"></i> Yeni Ticket
        </a>
    </nav>
</div>
```

#### 7. Gün (Yeni Ticket Oluşturma Sayfası)
**Yapılan İşler:**
- Form tasarımı
- Validasyon kontrolleri

**Açıklama:**
Kullanıcıların yeni ticket oluşturabileceği form tasarlandı.

**Kod Örneği:**
```html
<form method="POST" action="{{ url_for('new_ticket') }}">
    <div class="mb-3">
        <label class="form-label">Başlık</label>
        <input type="text" class="form-control" name="title" required>
    </div>
    <div class="mb-3">
        <label class="form-label">Açıklama</label>
        <textarea class="form-control" name="description" rows="5" required></textarea>
    </div>
    <div class="mb-3">
        <label class="form-label">Öncelik</label>
        <select class="form-select" name="priority">
            <option value="Düşük">Düşük</option>
            <option value="Normal">Normal</option>
            <option value="Yüksek">Yüksek</option>
        </select>
    </div>
    <button type="submit" class="btn btn-primary">Ticket Oluştur</button>
</form>
```

#### 8. Gün (Ticket Detay Sayfası)
**Yapılan İşler:**
- Ticket bilgileri görüntüleme
- Yanıt sistemi

**Açıklama:**
Ticket detaylarını görüntüleme ve yanıt verme özellikleri eklendi.

**Kod Örneği:**
```html
<div class="ticket-container">
    <div class="ticket-header">
        <h2>{{ ticket.title }}</h2>
        <span class="badge bg-{{ ticket.status_color }}">{{ ticket.status }}</span>
    </div>
    <div class="ticket-description">
        {{ ticket.description }}
    </div>
    <div class="ticket-responses">
        {% for response in ticket.responses %}
            <div class="response">
                <p>{{ response.content }}</p>
                <small>{{ response.created_at }}</small>
            </div>
        {% endfor %}
    </div>
</div>
```

#### 9. Gün (Admin Paneli Geliştirme)
**Yapılan İşler:**
- Admin yetkilendirme sistemi
- Ticket yönetimi

**Açıklama:**
Admin kullanıcılar için özel yönetim paneli oluşturuldu.

**Kod Örneği:**
```python
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('admin_dashboard.html', tickets=tickets)
```

#### 10. Gün (Veritabanı İşlemleri)
**Yapılan İşler:**
- CRUD operasyonları
- Veri bütünlüğü kontrolleri

**Açıklama:**
Veritabanı işlemleri için gerekli fonksiyonlar oluşturuldu.

**Kod Örneği:**
```python
def create_ticket(title, description, priority, user_id):
    ticket = Ticket(
        title=title,
        description=description,
        priority=priority,
        user_id=user_id
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket

def update_ticket_status(ticket_id, status):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = status
    db.session.commit()
    return ticket
```

#### 11. Gün (Güvenlik Önlemleri)
**Yapılan İşler:**
- Oturum yönetimi
- Yetkilendirme kontrolleri

**Açıklama:**
Uygulama güvenliği için gerekli önlemler alındı.

**Kod Örneği:**
```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def check_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.')
        return redirect(url_for('dashboard'))
```

#### 12. Gün (Responsive Tasarım İyileştirmeleri)
**Yapılan İşler:**
- Mobil uyumluluk
- Sidebar düzenlemesi

**Açıklama:**
Tüm sayfalar için responsive tasarım iyileştirmeleri yapıldı.

**Kod Örneği:**
```css
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-100%);
    }
    .main-content {
        margin-left: 0;
    }
    .sidebar.active {
        transform: translateX(0);
    }
}
```

#### 13. Gün (Kullanıcı Deneyimi İyileştirmeleri)
**Yapılan İşler:**
- Animasyonlar
- Hover efektleri

**Açıklama:**
Kullanıcı deneyimini artırmak için görsel iyileştirmeler yapıldı.

**Kod Örneği:**
```css
.ticket-card {
    transition: transform 0.3s ease;
}

.ticket-card:hover {
    transform: translateY(-5px);
}

.btn-primary {
    transition: all 0.3s ease;
}

.btn-primary:hover {
    transform: scale(1.05);
}
```

#### 14. Gün (Hata Yönetimi)
**Yapılan İşler:**
- 404 sayfası
- Hata mesajları

**Açıklama:**
Kullanıcı dostu hata sayfaları ve mesajları eklendi.

**Kod Örneği:**
```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

#### 15. Gün (Performans Optimizasyonu)
**Yapılan İşler:**
- Sayfa yükleme hızı
- Veritabanı sorguları

**Açıklama:**
Uygulama performansı için optimizasyonlar yapıldı.

**Kod Örneği:**
```python
# Veritabanı sorgularını optimize etme
tickets = Ticket.query.filter_by(user_id=current_user.id)\
    .order_by(Ticket.created_at.desc())\
    .limit(10)\
    .all()
```

#### 16. Gün (Test ve Hata Ayıklama)
**Yapılan İşler:**
- Unit testler
- Entegrasyon testleri

**Açıklama:**
Uygulama için test senaryoları yazıldı.

**Kod Örneği:**
```python
def test_login():
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 302
    assert response.location == '/dashboard'

def test_create_ticket():
    with client:
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        response = client.post('/ticket/new', data={
            'title': 'Test Ticket',
            'description': 'Test Description',
            'priority': 'Normal'
        })
        assert response.status_code == 302
```

#### 17. Gün (Dokümantasyon)
**Yapılan İşler:**
- Kod dokümantasyonu
- Kullanıcı kılavuzu

**Açıklama:**
Proje için gerekli dokümantasyonlar hazırlandı.

**Kod Örneği:**
```python
"""
HelpDesk Sistemi
---------------
Bu modül, HelpDesk sisteminin ana fonksiyonlarını içerir.

Classes:
    User: Kullanıcı modeli
    Ticket: Ticket modeli
    TicketResponse: Ticket yanıtları modeli

Functions:
    create_ticket: Yeni ticket oluşturur
    update_ticket_status: Ticket durumunu günceller
"""
```

#### 18. Gün (Son Kontroller)
**Yapılan İşler:**
- Güvenlik taraması
- Performans testleri

**Açıklama:**
Uygulama için son kontroller yapıldı.

#### 19. Gün (Deployment Hazırlığı)
**Yapılan İşler:**
- Sunucu yapılandırması
- Veritabanı yedekleme

**Açıklama:**
Uygulama deployment için hazırlandı.

#### 20. Gün (Proje Teslimi)
**Yapılan İşler:**
- Son kontroller
- Proje sunumu

**Açıklama:**
Proje tamamlandı ve teslim edildi.

### 1.3. Öğrenilen Teknolojiler
1. Python Flask Framework
2. SQLite Veritabanı
3. HTML5 ve CSS3
4. Bootstrap 5
5. Git Versiyon Kontrolü
6. Responsive Tasarım
7. RESTful API Tasarımı
8. JavaScript ve AJAX
9. Web Güvenliği
10. Test ve Debugging Araçları

### 1.4. Kazanılan Yetenekler
1. Full-stack web geliştirme
2. Veritabanı tasarımı ve yönetimi
3. Kullanıcı arayüzü tasarımı
4. Güvenlik önlemleri ve best practices
5. Test ve hata ayıklama
6. Proje yönetimi
7. Dokümantasyon
8. Takım çalışması
9. Problem çözme
10. Kod optimizasyonu

### 1.5. Staj Değerlendirmesi
Bu staj sürecinde, modern bir helpdesk sistemi geliştirerek hem teknik becerilerimi geliştirdim hem de gerçek dünya projesi deneyimi kazandım. Sistem, kullanıcı dostu arayüzü ve güvenli backend yapısıyla profesyonel bir destek yönetim sistemi olarak hizmet verebilir durumdadır. Staj süresince öğrendiğim teknolojiler ve kazandığım deneyimler, gelecekteki kariyerim için değerli bir temel oluşturmuştur.

## Staj Günlüğü
[Her gün için ayrı ayrı doldurulacak]

## Formlar
[Staj yapılan kurum tarafından doldurulacak] 