# KIRIKKALE ÜNİVERSİTESİ
## MÜHENDİSLİK FAKÜLTESİ
### BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ
#### STAJ DOSYASI

**Öğrenci Bilgileri:**
- Ad Soyad: [Öğrenci Adı Soyadı]
- Öğrenci No: [Öğrenci Numarası]
- Staj Süresi: 20 İş Günü
- Staj Tarihi: [Tarih Aralığı]
- Staj Yeri: [Şirket Adı]
- Staj Türü: İşyeri Stajı

## İÇİNDEKİLER
1. [Staj Yapılan Kurum Hakkında Bilgi](#staj-yapılan-kurum-hakkında-bilgi)
2. [Staj Süresince Yapılan İşler](#staj-süresince-yapılan-işler)
3. [Öğrenilen Teknolojiler](#öğrenilen-teknolojiler)
4. [Kazanılan Yetenekler](#kazanılan-yetenekler)
5. [Staj Değerlendirmesi](#staj-değerlendirmesi)
6. [Staj Günlüğü](#staj-günlüğü)
7. [Formlar](#formlar)

## Staj Yapılan Kurum Hakkında Bilgi
- Kurum Adı: [Şirket Adı]
- Kurum Adresi: [Şirket Adresi]
- Kurumun Faaliyet Alanı: Yazılım Geliştirme ve Teknoloji Çözümleri
- Kurumun Web Sitesi: [Web Sitesi]

## Staj Süresince Yapılan İşler

### 1. Gün
**Yapılan İşler:**
- Proje tanımı ve kapsamının belirlenmesi
- Gerekli teknolojilerin seçimi
- Temel özelliklerin belirlenmesi

**Açıklama:**
HelpDesk sistemi için kapsamlı bir proje planı oluşturuldu. Modern web teknolojileri kullanılarak kullanıcı dostu bir arayüz tasarlanacak. Sistem, müşteri destek taleplerinin etkin bir şekilde yönetilmesini sağlayacak. Projenin temel özellikleri şunlardır:
- Kullanıcı kaydı ve girişi
- Destek talebi oluşturma ve takibi
- Öncelik seviyelerine göre taleplerin sıralanması
- Admin paneli ile yönetim
- Gerçek zamanlı bildirimler
- Detaylı raporlama sistemi

**Kullanılan Teknolojiler:**
- Python
- Flask
- SQLite
- Bootstrap 5

### 2. Gün
**Yapılan İşler:**
- Veritabanı modellerinin oluşturulması
- İlişkisel veritabanı yapısının tasarlanması

**Açıklama:**
SQLite veritabanı kullanılarak kapsamlı bir veri modeli tasarlandı. Sistem şu ana modelleri içermektedir:
- Kullanıcılar (Users): Sistem kullanıcılarının bilgileri
- Destek Talepleri (Tickets): Müşteri destek talepleri
- Yanıtlar (Responses): Taleplere verilen yanıtlar
- Kategoriler (Categories): Destek taleplerinin kategorileri
- Öncelikler (Priorities): Taleplerin öncelik seviyeleri
- Durumlar (Statuses): Taleplerin mevcut durumları

Her model için gerekli ilişkiler ve kısıtlamalar tanımlandı. Veritabanı şeması, sistemin ölçeklenebilirliğini ve performansını göz önünde bulundurarak tasarlandı.

**Kullanılan Teknolojiler:**
- SQLAlchemy
- SQLite

### 3. Gün
**Yapılan İşler:**
- Flask framework'ünün kurulumu
- Proje yapısının oluşturulması

**Açıklama:**
Flask uygulaması için kapsamlı bir yapılandırma yapıldı. Proje yapısı şu şekilde organize edildi:
- templates/: HTML şablonları
- static/: CSS, JavaScript ve medya dosyaları
- models/: Veritabanı modelleri
- routes/: URL yönlendirmeleri
- utils/: Yardımcı fonksiyonlar
- config.py: Yapılandırma ayarları

Güvenlik önlemleri alındı:
- CSRF koruması
- Şifre hashleme
- Oturum yönetimi
- Güvenli dosya yükleme
- XSS koruması

**Kullanılan Teknolojiler:**
- Flask
- Python

### 4. Gün
**Yapılan İşler:**
- Ana sayfa tasarımı
- Bootstrap entegrasyonu

**Açıklama:**
Ana sayfa için modern ve kullanıcı dostu bir arayüz tasarlandı. Tasarım şu özellikleri içeriyor:
- Responsive navbar
- Hero section ile dikkat çekici giriş
- Özellikler bölümü
- İstatistikler bölümü
- Footer bölümü

Kullanıcı deneyimi iyileştirmeleri:
- Smooth scroll
- Hover efektleri
- Loading animasyonları
- Responsive grid sistem
- Modern renk paleti

**Kullanılan Teknolojiler:**
- HTML5
- CSS3
- Bootstrap 5

### 5. Gün
**Yapılan İşler:**
- Giriş sayfası tasarımı
- Güvenlik kontrolleri

**Açıklama:**
Güvenli ve kullanıcı dostu bir giriş sayfası tasarlandı. Sayfa şu özellikleri içeriyor:
- Modern form tasarımı
- Input validasyonu
- Hata mesajları
- "Beni hatırla" seçeneği
- Şifremi unuttum linki
- Sosyal medya ile giriş seçenekleri

Güvenlik önlemleri:
- Brute force koruması
- IP bazlı kısıtlamalar
- İki faktörlü doğrulama
- Güvenli oturum yönetimi

**Kullanılan Teknolojiler:**
- Flask-Login
- WTForms

### 6. Gün
**Yapılan İşler:**
- Dashboard sayfası tasarımı
- Sidebar menü

**Açıklama:**
Kullanıcıların ticketlarını yönetebileceği kapsamlı bir dashboard sayfası tasarlandı. Özellikler:
- Dinamik sidebar menü
- Ticket filtreleme ve arama
- Sıralama seçenekleri
- İstatistik kartları
- Grafik ve raporlar
- Bildirim sistemi

Kullanıcı deneyimi iyileştirmeleri:
- Drag & drop sıralama
- Gerçek zamanlı güncelleme
- Özelleştirilebilir görünüm
- Klavye kısayolları

**Kullanılan Teknolojiler:**
- Bootstrap 5
- JavaScript

### 7. Gün
**Yapılan İşler:**
- Yeni ticket oluşturma formu
- Validasyon kontrolleri

**Açıklama:**
Kullanıcıların yeni ticket oluşturabileceği kapsamlı bir form tasarlandı. Özellikler:
- Çoklu kategori seçimi
- Dosya yükleme
- Zengin metin editörü
- Otomatik kaydetme
- Taslak oluşturma
- Şablon seçenekleri

Validasyon kontrolleri:
- Zorunlu alan kontrolü
- Dosya boyutu ve türü kontrolü
- XSS koruması
- Spam koruması

**Kullanılan Teknolojiler:**
- WTForms
- Flask-WTF

### 8. Gün
**Yapılan İşler:**
- Ticket detay sayfası
- Yanıt sistemi

**Açıklama:**
Ticket detaylarını görüntüleme ve yanıt verme özellikleri eklendi. Sayfa şu özellikleri içeriyor:
- Ticket durumu ve önceliği
- Oluşturulma ve güncellenme tarihleri
- Yanıt geçmişi
- Dosya ekleri
- Etiketler
- İşlem geçmişi

Yanıt sistemi özellikleri:
- Zengin metin editörü
- Dosya ekleme
- İç yanıtlar
- Yanıt şablonları
- Otomatik bildirimler

**Kullanılan Teknolojiler:**
- Flask
- SQLAlchemy

### 9. Gün
**Yapılan İşler:**
- Admin paneli
- Yetkilendirme sistemi

**Açıklama:**
Admin kullanıcılar için kapsamlı bir yönetim paneli oluşturuldu. Özellikler:
- Kullanıcı yönetimi
- Ticket yönetimi
- Kategori yönetimi
- Sistem ayarları
- Raporlama araçları
- Log görüntüleme

Yetkilendirme sistemi:
- Rol tabanlı erişim kontrolü
- İzin yönetimi
- Aktivite logları
- Güvenlik denetimi

**Kullanılan Teknolojiler:**
- Flask-Login
- Flask-Admin

### 10. Gün
**Yapılan İşler:**
- Veritabanı işlemleri
- CRUD operasyonları

**Açıklama:**
Veritabanı işlemleri için kapsamlı fonksiyonlar oluşturuldu. Özellikler:
- Veri ekleme
- Veri güncelleme
- Veri silme
- Veri listeleme
- İlişkisel sorgular
- Toplu işlemler

Veri bütünlüğü kontrolleri:
- Foreign key kontrolleri
- Unique constraint kontrolleri
- Cascade işlemleri
- Transaction yönetimi
- Veri doğrulama

**Kullanılan Teknolojiler:**
- SQLAlchemy
- SQLite

### 11. Gün
**Yapılan İşler:**
- Güvenlik önlemleri
- Oturum yönetimi

**Açıklama:**
Uygulama güvenliği için kapsamlı önlemler alındı. Özellikler:
- Güvenli oturum yönetimi
- Şifreleme
- XSS koruması
- CSRF koruması
- SQL injection koruması
- Dosya yükleme güvenliği

Yetkilendirme sistemi:
- Rol tabanlı erişim
- İzin yönetimi
- Aktivite logları
- Güvenlik denetimi
- IP kısıtlamaları

**Kullanılan Teknolojiler:**
- Flask-Security
- Werkzeug

### 12. Gün
**Yapılan İşler:**
- Responsive tasarım
- Mobil uyumluluk

**Açıklama:**
Tüm sayfalar için kapsamlı responsive tasarım iyileştirmeleri yapıldı. Özellikler:
- Mobil öncelikli tasarım
- Esnek grid sistemi
- Dinamik sidebar
- Touch-friendly arayüz
- Responsive görüntüler
- Performans optimizasyonu

Kullanıcı deneyimi iyileştirmeleri:
- Gesture desteği
- Offline kullanım
- Progressive loading
- Adaptive layout

**Kullanılan Teknolojiler:**
- Bootstrap 5
- CSS3

### 13. Gün
**Yapılan İşler:**
- Kullanıcı deneyimi
- Animasyonlar

**Açıklama:**
Kullanıcı deneyimini artırmak için kapsamlı görsel iyileştirmeler yapıldı. Özellikler:
- Smooth animasyonlar
- Hover efektleri
- Loading states
- Transitions
- Micro-interactions
- Visual feedback

Performans optimizasyonları:
- Lazy loading
- Image optimization
- Code splitting
- Caching
- Bundle optimization

**Kullanılan Teknolojiler:**
- CSS3
- JavaScript

### 14. Gün
**Yapılan İşler:**
- Hata yönetimi
- 404 sayfası

**Açıklama:**
Kullanıcı dostu hata sayfaları ve mesajları eklendi. Özellikler:
- Özelleştirilmiş hata sayfaları
- Detaylı hata mesajları
- Hata loglama
- Hata raporlama
- Otomatik bildirimler
- Kullanıcı yönlendirme

Hata yönetimi:
- Exception handling
- Error tracking
- Debug mode
- Log rotation
- Error analytics

**Kullanılan Teknolojiler:**
- Flask
- HTML5

### 15. Gün
**Yapılan İşler:**
- Performans optimizasyonu
- Veritabanı sorguları

**Açıklama:**
Uygulama performansı için kapsamlı optimizasyonlar yapıldı. Özellikler:
- Database query optimization
- Caching
- Asset optimization
- Code minification
- Lazy loading
- Connection pooling

Performans metrikleri:
- Load time
- Time to first byte
- First contentful paint
- Time to interactive
- Memory usage
- CPU usage

**Kullanılan Teknolojiler:**
- SQLAlchemy
- Flask-Caching

### 16. Gün
**Yapılan İşler:**
- Test senaryoları
- Hata ayıklama

**Açıklama:**
Uygulama için kapsamlı test senaryoları yazıldı. Test türleri:
- Unit tests
- Integration tests
- Functional tests
- Performance tests
- Security tests
- UI tests

Test araçları:
- pytest
- unittest
- Selenium
- JMeter
- OWASP ZAP
- Lighthouse

**Kullanılan Teknolojiler:**
- pytest
- unittest

### 17. Gün
**Yapılan İşler:**
- Dokümantasyon
- Kullanıcı kılavuzu

**Açıklama:**
Proje için kapsamlı dokümantasyonlar hazırlandı. Dokümantasyon türleri:
- API documentation
- User manual
- Installation guide
- Development guide
- Deployment guide
- Troubleshooting guide

Dokümantasyon araçları:
- Sphinx
- MkDocs
- Swagger
- Postman
- Draw.io
- GitBook

**Kullanılan Teknolojiler:**
- Sphinx
- Markdown

### 18. Gün
**Yapılan İşler:**
- Son kontroller
- Güvenlik taraması

**Açıklama:**
Uygulama için kapsamlı son kontroller yapıldı. Kontrol alanları:
- Güvenlik açıkları
- Performans sorunları
- Kod kalitesi
- Dokümantasyon
- Test coverage
- Kullanıcı deneyimi

Kullanılan araçlar:
- SonarQube
- OWASP ZAP
- Lighthouse
- GTmetrix
- ESLint
- Prettier

**Kullanılan Teknolojiler:**
- Bandit
- Safety

### 19. Gün
**Yapılan İşler:**
- Deployment hazırlığı
- Sunucu yapılandırması

**Açıklama:**
Uygulama deployment için kapsamlı hazırlıklar yapıldı. Hazırlık alanları:
- Sunucu konfigürasyonu
- SSL sertifikası
- Domain ayarları
- Backup sistemi
- Monitoring
- Logging

Kullanılan teknolojiler:
- Docker
- Nginx
- Let's Encrypt
- AWS
- Prometheus
- Grafana

**Kullanılan Teknolojiler:**
- Gunicorn
- Nginx

### 20. Gün
**Yapılan İşler:**
- Proje sunumu
- Son kontroller

**Açıklama:**
Proje kapsamlı bir şekilde tamamlandı ve teslim edildi. Teslim süreci:
- Kod review
- Dokümantasyon kontrolü
- Test sonuçları
- Performans raporu
- Güvenlik raporu
- Kullanıcı kabulü

Proje başarıları:
- Modern teknolojiler
- Güvenli yapı
- Performanslı sistem
- Kullanıcı dostu arayüz
- Ölçeklenebilir mimari
- Kolay bakım

**Kullanılan Teknolojiler:**
- Git
- GitHub

## Öğrenilen Teknolojiler
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

## Kazanılan Yetenekler
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

## Staj Değerlendirmesi
Bu staj sürecinde, modern bir helpdesk sistemi geliştirerek hem teknik becerilerimi geliştirdim hem de gerçek dünya projesi deneyimi kazandım. Sistem, kullanıcı dostu arayüzü ve güvenli backend yapısıyla profesyonel bir destek yönetim sistemi olarak hizmet verebilir durumdadır. Staj süresince öğrendiğim teknolojiler ve kazandığım deneyimler, gelecekteki kariyerim için değerli bir temel oluşturmuştur.

## Staj Günlüğü
[Staj günlüğü ayrı bir dosyada tutulacaktır]

## Formlar
[Staj yapılan kurum tarafından doldurulacak] 