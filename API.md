# API Dokümantasyonu

Bu dokümantasyon, AI Help Desk sisteminin API endpoint'lerini ve kullanımlarını açıklar.

## Kimlik Doğrulama

Tüm API istekleri için JWT token gereklidir. Token'ı request header'ında şu şekilde gönderin:

```
Authorization: Bearer <token>
```

## Endpoints

### Kullanıcı İşlemleri

#### Kayıt Olma
```http
POST /api/register
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string"
}
```

**Yanıt:**
```json
{
    "message": "Kayıt başarılı",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string"
    }
}
```

#### Giriş Yapma
```http
POST /api/login
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

**Yanıt:**
```json
{
    "token": "string",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "is_admin": "boolean"
    }
}
```

### Ticket İşlemleri

#### Ticket Listesi
```http
GET /api/tickets
Authorization: Bearer <token>
```

**Yanıt:**
```json
{
    "tickets": [
        {
            "id": "integer",
            "title": "string",
            "description": "string",
            "status": "string",
            "priority": "string",
            "category": "string",
            "created_at": "datetime",
            "user": {
                "id": "integer",
                "username": "string"
            }
        }
    ]
}
```

#### Yeni Ticket Oluşturma
```http
POST /api/tickets
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "string",
    "description": "string",
    "priority": "string",
    "category": "string"
}
```

**Yanıt:**
```json
{
    "message": "Ticket oluşturuldu",
    "ticket": {
        "id": "integer",
        "title": "string",
        "description": "string",
        "status": "string",
        "priority": "string",
        "category": "string",
        "created_at": "datetime"
    }
}
```

#### Ticket Detayı
```http
GET /api/tickets/{ticket_id}
Authorization: Bearer <token>
```

**Yanıt:**
```json
{
    "ticket": {
        "id": "integer",
        "title": "string",
        "description": "string",
        "status": "string",
        "priority": "string",
        "category": "string",
        "created_at": "datetime",
        "user": {
            "id": "integer",
            "username": "string"
        },
        "responses": [
            {
                "id": "integer",
                "content": "string",
                "created_at": "datetime",
                "user": {
                    "id": "integer",
                    "username": "string"
                }
            }
        ],
        "status_history": [
            {
                "id": "integer",
                "old_status": "string",
                "new_status": "string",
                "changed_at": "datetime",
                "changed_by": {
                    "id": "integer",
                    "username": "string"
                }
            }
        ]
    }
}
```

#### Ticket Yanıtı Ekleme
```http
POST /api/tickets/{ticket_id}/responses
Authorization: Bearer <token>
Content-Type: application/json

{
    "content": "string"
}
```

**Yanıt:**
```json
{
    "message": "Yanıt eklendi",
    "response": {
        "id": "integer",
        "content": "string",
        "created_at": "datetime",
        "user": {
            "id": "integer",
            "username": "string"
        }
    }
}
```

#### Ticket Durumu Güncelleme
```http
POST /api/tickets/{ticket_id}/status
Authorization: Bearer <token>
Content-Type: application/json

{
    "status": "string",
    "note": "string"
}
```

**Yanıt:**
```json
{
    "message": "Durum güncellendi",
    "ticket": {
        "id": "integer",
        "status": "string"
    }
}
```

### AI API

#### Kategori ve Yanıt Önerisi
```http
POST /api/ai/suggest
Authorization: Bearer <token>
Content-Type: application/json

{
    "text": "string"
}
```

**Yanıt:**
```json
{
    "category": "string",
    "auto_response": {
        "response": "string",
        "confidence": "float"
    }
}
```

## Hata Kodları

- 400: Geçersiz İstek
- 401: Yetkisiz Erişim
- 403: Erişim Reddedildi
- 404: Bulunamadı
- 500: Sunucu Hatası

## Örnek Kullanım

```python
import requests

# API endpoint'i
BASE_URL = "http://localhost:5000/api"

# Giriş yapma
login_response = requests.post(f"{BASE_URL}/login", json={
    "username": "admin",
    "password": "admin123"
})
token = login_response.json()["token"]

# Yeni ticket oluşturma
headers = {"Authorization": f"Bearer {token}"}
ticket_response = requests.post(f"{BASE_URL}/tickets", 
    headers=headers,
    json={
        "title": "Yazıcı Sorunu",
        "description": "Yazıcı çalışmıyor",
        "priority": "high",
        "category": "Donanım"
    }
) 