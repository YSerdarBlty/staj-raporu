# Katkıda Bulunma Rehberi

Bu projeye katkıda bulunmak istediğiniz için teşekkür ederiz! Bu rehber, projeye nasıl katkıda bulunabileceğinizi açıklamaktadır.

## Geliştirme Ortamı Kurulumu

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

## Kod Standartları

- PEP 8 standartlarına uyun
- Tüm yeni fonksiyonlar için docstring ekleyin
- Değişken ve fonksiyon isimleri anlamlı olmalı
- Kodunuzu test edin
- Gereksiz yorum satırlarından kaçının

## Git İş Akışı

1. Yeni bir branch oluşturun:
```bash
git checkout -b feature/yeni-ozellik
```

2. Değişikliklerinizi commit edin:
```bash
git add .
git commit -m "Yeni özellik: Açıklama"
```

3. Branch'inizi push edin:
```bash
git push origin feature/yeni-ozellik
```

4. Pull Request oluşturun

## Pull Request Süreci

1. Pull request şablonunu kullanın
2. Tüm testlerin başarılı olduğundan emin olun
3. Kodunuzu gözden geçirin
4. Gerekli dokümantasyon güncellemelerini yapın
5. Review bekleyin

## Test

- Yeni özellikler için test yazın
- Mevcut testleri güncelleyin
- Tüm testlerin başarılı olduğundan emin olun

## Dokümantasyon

- README.md dosyasını güncelleyin
- CHANGELOG.md dosyasını güncelleyin
- API.md dosyasını güncelleyin (API değişiklikleri varsa)
- Yeni özellikler için kullanım kılavuzu ekleyin

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Katkıda bulunarak, katkılarınızın aynı lisans altında yayınlanmasını kabul etmiş olursunuz.

## İletişim

Sorularınız veya önerileriniz için:
- Issue açın
- Pull request gönderin
- E-posta gönderin: ornek@email.com

## Teşekkürler

Projeye katkıda bulunduğunuz için teşekkür ederiz! 