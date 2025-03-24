# AI Destekli Help Desk Sistemi

Bu proje, yapay zeka destekli bir help desk yönetim sistemidir. Kullanıcıların destek taleplerini oluşturmasına, yönetmesine ve yapay zeka ile desteklenen yanıtlar almasına olanak sağlar.

## Özellikler

- 👤 Kullanıcı yönetimi (kayıt, giriş, profil)
- 🎫 Ticket yönetimi (oluşturma, görüntüleme, güncelleme)
- 🤖 AI destekli kategori önerisi
- 💬 AI destekli yanıt önerisi
- 📊 Dashboard ve istatistikler
- 🔒 Rol tabanlı yetkilendirme
- 📱 Responsive tasarım
- 🔄 Gerçek zamanlı durum güncellemeleri

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/kullaniciadi/ai-helpdesk.git
cd ai-helpdesk
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac için
venv\Scripts\activate     # Windows için
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanını oluşturun:
```bash
python -c "from app import db, app; app.app_context().push(); db.create_all()"
```

5. Uygulamayı çalıştırın:
```bash
python app.py
```

6. Tarayıcınızda `http://127.0.0.1:5000` adresine gidin

## Varsayılan Kullanıcı Bilgileri

- Admin Kullanıcısı:
  - Kullanıcı adı: `admin`
  - Şifre: `admin123`

## Teknolojiler

- Python 3.8+
- Flask
- SQLAlchemy
- OpenAI API
- Bootstrap 5
- jQuery
- Chart.js

## Katkıda Bulunma

Projeye katkıda bulunmak için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını inceleyin.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Güvenlik

Güvenlik politikamız hakkında bilgi için [SECURITY.md](SECURITY.md) dosyasını inceleyin.

## API Dokümantasyonu

API endpoint'leri ve kullanımı hakkında bilgi için [API.md](API.md) dosyasını inceleyin.

## Değişiklik Günlüğü

Projedeki önemli değişiklikler için [CHANGELOG.md](CHANGELOG.md) dosyasını inceleyin.

## İletişim

- Website: [https://ai-helpdesk.com](https://ai-helpdesk.com)
- E-posta: ornek@email.com
- Twitter: [@aihelpdesk](https://twitter.com/aihelpdesk)
- GitHub: [github.com/kullaniciadi/ai-helpdesk](https://github.com/kullaniciadi/ai-helpdesk) 