# Backend API - Sentiment & Readability Analysis

## ✅ Status: READY TO USE!

Backend API sudah siap digunakan dengan **Laravel 10** dan **PHP 8.1**!

---

## 🚀 Cara Menjalankan Backend

### **Metode 1: PHP Built-in Server (Untuk Development)**

```bash
cd backend/public
php -S localhost:8000
```

Server akan jalan di: **http://localhost:8000**

### **Metode 2: XAMPP Apache (Untuk Production-like)**

1. Copy folder `backend` ke `C:\xampp\htdocs\`
2. Buka XAMPP Control Panel
3. Start Apache
4. Akses di: **http://localhost/backend/public/api.php**

---

## 📡 API Endpoint

### **POST /api.php**

**URL:** `http://localhost:8000/api.php`

**Headers:**
```
Content-Type: application/json
```

### **Request Format 1: Text Input (JSON)**

```json
{
  "text": "Presiden memberikan bantuan kepada rakyat. Program ini sangat bagus."
}
```

### **Request Format 2: File Upload (Form Data)**

```bash
curl -X POST http://localhost:8000/api.php \
  -F "file=@berita.txt"
```

**Supported file types:**
- `.txt` ✅ (Working)
- `.pdf` ⏳ (Coming soon)
- `.docx` ⏳ (Coming soon)

---

## 📥 Response Format

```json
{
    "success": true,
    "text": "Presiden memberikan bantuan...",
    "sentiment": "Positive",
    "sentiment_score": 0.75,
    "sentiment_details": "Analisis lengkap dari Gemini AI...",
    "readability": 65.5,
    "readability_category": "Standar",
    "word_count": 13,
    "sentence_count": 2
}
```

### **Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Status request (true/false) |
| `text` | string | Teks yang dianalisis (dipotong 500 karakter) |
| `sentiment` | string | Hasil: "Positive", "Negative", "Neutral" |
| `sentiment_score` | float | Skor 0-1 (0=negatif, 1=positif) |
| `sentiment_details` | string | Penjelasan dari Gemini AI |
| `readability` | float | Skor Flesch Reading Ease |
| `readability_category` | string | Kategori keterbacaan |
| `word_count` | int | Jumlah kata |
| `sentence_count` | int | Jumlah kalimat |

### **Readability Categories:**

| Score | Category |
|-------|----------|
| 90-100 | Sangat Mudah |
| 80-89 | Mudah |
| 70-79 | Cukup Mudah |
| 60-69 | Standar |
| 50-59 | Cukup Sulit |
| 30-49 | Sulit |
| 0-29 | Sangat Sulit |

---

## 🧪 Testing dengan curl

### **Test 1: Berita Positif**
```bash
curl -X POST http://localhost:8000/api.php \
  -H "Content-Type: application/json" \
  -d '{"text":"Presiden memberikan bantuan kepada rakyat. Program ini sangat bagus dan meningkatkan kesejahteraan masyarakat."}'
```

### **Test 2: Berita Negatif**
```bash
curl -X POST http://localhost:8000/api.php \
  -H "Content-Type: application/json" \
  -d '{"text":"Korupsi merajalela di pemerintahan. Rakyat sangat kecewa dengan kebijakan yang buruk."}'
```

### **Test 3: File Upload**
```bash
# Buat file test
echo "ITS Surabaya meraih prestasi gemilang di kompetisi internasional." > test.txt

# Upload file
curl -X POST http://localhost:8000/api.php \
  -F "file=@test.txt"
```

---

## 🔧 Konfigurasi

### **File: `backend/.env`**

```env
# Gemini API Configuration
GEMINI_API_KEY=AIzaSyBF-YrSXhCODSZFYDyvx-0KzKIljYGmAGs
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent
```

**Cara ganti API key:**
1. Buka file `backend/.env`
2. Ubah value `GEMINI_API_KEY`
3. Save & restart server

---

## 🌐 CORS Support

API sudah dilengkapi CORS headers untuk frontend:

```php
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

Frontend dari domain manapun bisa akses API ini.

---

## 🔄 Integrasi dengan Frontend Vue.js

### **Di Frontend (Vue.js):**

```javascript
// services/api.js
const API_URL = 'http://localhost:8000/api.php';

export async function analyzeText(text) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text })
  });

  return await response.json();
}

export async function analyzeFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(API_URL, {
    method: 'POST',
    body: formData
  });

  return await response.json();
}
```

### **Contoh Penggunaan:**

```javascript
import { analyzeText } from './services/api';

// Di component Vue
async function handleAnalyze() {
  const result = await analyzeText(inputText.value);

  sentiment.value = result.sentiment;
  sentimentScore.value = result.sentiment_score;
  readability.value = result.readability;
}
```

---

## ⚙️ Teknologi yang Digunakan

- **PHP 8.1** (Pure PHP, no framework dependency untuk API)
- **Gemini 2.0 Flash API** (Sentiment Analysis)
- **Flesch Reading Ease Algorithm** (Readability Analysis)
- **cURL** (HTTP Client untuk Gemini API)

---

## 🐛 Troubleshooting

### **Error: "Connection refused"**
- Pastikan server jalan: `php -S localhost:8000`
- Cek port tidak bentrok

### **Error: "API key invalid"**
- Cek file `.env` ada API key yang benar
- Restart server setelah ubah `.env`

### **Error: "CORS policy"**
- Header CORS sudah ada di `api.php`
- Pastikan browser tidak block request

### **Response: Fallback analysis**
- Gemini API mungkin error/timeout
- API akan otomatis pakai analisis sederhana (keyword-based)

---

## 📞 Untuk Customer/Demo

**Jalankan server:**
```bash
cd backend/public
php -S localhost:8000
```

**Test di browser** (Postman alternative):
1. Buka: https://hoppscotch.io/
2. Method: POST
3. URL: `http://localhost:8000/api.php`
4. Body → Raw (JSON):
   ```json
   {
     "text": "Berita test untuk analisis sentimen"
   }
   ```
5. Send!

---

## ✅ Checklist untuk Production

- [ ] Ganti Gemini API key dengan akun customer
- [ ] Setup proper web server (Apache/Nginx)
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Add API authentication (optional)
- [ ] Implement PDF/DOCX parser
- [ ] Add logging & monitoring

---

🎉 **Backend sudah READY untuk demo ke customer!**
