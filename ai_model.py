import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AIHelpDesk:
    def __init__(self):
        # Bilgi tabanını yükle
        self.knowledge_base = self.load_knowledge_base()
        
        # TF-IDF vektörleştirici
        self.vectorizer = TfidfVectorizer()
        
        # Bilgi tabanındaki tüm metinleri vektörleştir
        self.texts = []
        self.qa_pairs = []
        
        for category, data in self.knowledge_base.items():
            for qa_pair in data['qa_pairs']:
                self.texts.append(qa_pair['soru'])
                self.qa_pairs.append(qa_pair)
        
        if self.texts:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.texts)
    
    def load_knowledge_base(self):
        kb_file = 'knowledge_base.json'
        if os.path.exists(kb_file):
            with open(kb_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "genel": {
                "context": """
                Help Desk sistemi, kullanıcıların teknik sorunlarını çözmek için tasarlanmış bir destek platformudur.
                Kullanıcılar ticket açabilir, yöneticiler yanıt verebilir.
                Ticketlar farklı kategorilerde ve öncelik seviyelerinde olabilir.
                """,
                "qa_pairs": [
                    {
                        "soru": "Nasıl yeni ticket açabilirim?",
                        "cevap": "Dashboard'da 'Yeni Ticket' butonuna tıklayarak başlık, kategori, öncelik ve açıklama girmeniz gerekiyor."
                    },
                    {
                        "soru": "Ticket durumları ne anlama geliyor?",
                        "cevap": "Açık: Yeni açılmış ticket, İşlemde: İnceleniyor, Beklemede: Ek bilgi bekleniyor, Çözüldü: Sorun giderildi, Kapalı: İşlem tamamlandı."
                    }
                ]
            }
        }
    
    def analyze_text(self, text):
        """Metni analiz eder ve önemli bilgileri çıkarır"""
        # Basit anahtar kelime analizi
        words = text.lower().split()
        return {
            'keywords': [word for word in words if len(word) > 3],
            'sentiment': 'positive' if any(word in ['çalışıyor', 'iyi', 'tamam'] for word in words) 
                       else 'negative' if any(word in ['çalışmıyor', 'hata', 'sorun'] for word in words)
                       else 'neutral'
        }
    
    def get_auto_response(self, ticket_text):
        """Ticket metnine otomatik yanıt önerir"""
        if not self.texts:
            return {
                'response': 'Üzgünüm, henüz yeterli bilgi yok.',
                'confidence': 0.0,
                'analysis': self.analyze_text(ticket_text)
            }
        
        # Metni vektörleştir
        query_vector = self.vectorizer.transform([ticket_text])
        
        # Benzerlik skorlarını hesapla
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        
        # En yüksek benzerlik skoruna sahip yanıtı bul
        best_idx = similarities.argmax()
        best_score = similarities[best_idx]
        best_response = self.qa_pairs[best_idx]['cevap']
        
        return {
            'response': best_response,
            'confidence': float(best_score),
            'analysis': self.analyze_text(ticket_text)
        }
    
    def suggest_category(self, ticket_text):
        """Ticket metni için kategori önerir"""
        analysis = self.analyze_text(ticket_text)
        keywords = analysis['keywords']
        
        categories = {
            'Teknik Destek': ['hata', 'çalışmıyor', 'bozuk', 'sorun'],
            'Yazılım': ['program', 'uygulama', 'yazılım', 'güncelleme'],
            'Donanım': ['bilgisayar', 'ekran', 'fare', 'klavye', 'printer'],
            'Ağ': ['internet', 'bağlantı', 'wifi', 'ağ'],
        }
        
        max_score = 0
        suggested_category = 'Diğer'
        
        for category, category_keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in category_keywords)
            if score > max_score:
                max_score = score
                suggested_category = category
        
        return suggested_category
    
    def update_knowledge_base(self, ticket):
        """Çözülmüş ticketlardan öğrenme"""
        if ticket.status == 'Çözüldü' and ticket.responses:
            # Son yanıtı al
            last_response = ticket.responses[-1]
            
            # Yeni soru-cevap çifti oluştur
            new_qa_pair = {
                "soru": ticket.description,
                "cevap": last_response.content
            }
            
            # Kategoriye göre bilgi tabanını güncelle
            if ticket.category not in self.knowledge_base:
                self.knowledge_base[ticket.category] = {
                    "context": f"{ticket.category} ile ilgili sorunlar ve çözümleri.",
                    "qa_pairs": []
                }
            
            self.knowledge_base[ticket.category]["qa_pairs"].append(new_qa_pair)
            
            # Bilgi tabanını kaydet
            with open('knowledge_base.json', 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=4)
            
            # Vektörleştiriciyi güncelle
            self.texts.append(new_qa_pair['soru'])
            self.qa_pairs.append(new_qa_pair)
            self.tfidf_matrix = self.vectorizer.fit_transform(self.texts) 