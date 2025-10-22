# Panduan Integrasi - Sentiment & Readability Analysis

Panduan lengkap untuk menjalankan aplikasi analisis sentimen dan readability yang telah terintegrasi.

## 📋 Prerequisites

### Software yang Dibutuhkan
- **Node.js** (v18 atau lebih baru) - untuk frontend
- **PHP** (v8.1 atau lebih baru) - untuk backend
- **Python** (v3.10 atau lebih baru) - untuk ML scripts
- **Git** (optional)

## 🔑 API Keys

Aplikasi ini sudah dikonfigurasi dengan API keys berikut:

- **Gemini API**: `AIzaSyBIh8y9NibKTSKMvL2FpoxMPo2sWYCIOVk`
- **DeepSeek API**: `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`
- **OCR API**: `K81288052388957`
- **HuggingFace BERT**: `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`

API keys sudah tersimpan di file `.env` masing-masing folder.

## 🚀 Cara Menjalankan Aplikasi

### 1️⃣ Backend (Laravel/PHP API)

```bash
# Masuk ke folder backend
cd Sentiment-ReadAbility-Analysis-of-News-Website-main/backend/public

# Jalankan PHP built-in server
php -S localhost:8000

# Server akan berjalan di: http://localhost:8000
```

**Test Backend API:**
```bash
# Test dengan curl
curl -X POST http://localhost:8000/api.php \
  -H "Content-Type: application/json" \
  -d '{"text": "Presiden memberikan bantuan kepada rakyat yang membutuhkan"}'
```

Expected response:
```json
{
  "success": true,
  "text": "Presiden memberikan bantuan kepada rakyat...",
  "sentiment": "Positive",
  "sentiment_score": 0.75,
  "sentiment_details": "Sentimen: Positif, Alasan: ...",
  "readability": 65.5,
  "readability_category": "Standar",
  "word_count": 8,
  "sentence_count": 1
}
```

### 2️⃣ Frontend (Vue.js 3)

**Buka terminal baru:**

```bash
# Masuk ke folder frontend
cd Sentiment-ReadAbility-Analysis-of-News-Website-main/frontend

# Install dependencies (hanya perlu sekali)
npm install

# Jalankan development server
npm run dev

# Frontend akan berjalan di: http://localhost:5173
```

**Build untuk production:**
```bash
npm run build
npm run preview
```

### 3️⃣ ML Scripts (Python)

**Install dependencies:**
```bash
cd Sentiment-ReadAbility-Analysis-of-News-Website-main/ml

# Install required packages
pip install requests beautifulsoup4 python-dotenv
```

**Jalankan script analisis:**

```bash
# Analisis dari file teks
python PBKK_script_api.py berita.txt

# Analisis dari file HTML
python PBKK_script_api.py berita.html

# Analisis dari gambar (dengan OCR)
python PBKK_script_api.py berita.png

# Bandingkan hasil dari 3 API (Gemini, DeepSeek, BERT)
python PBKK_script_api.py berita.txt --compare
```

**Script sederhana dengan Gemini saja:**
```bash
python script_gemini.py
```

## 📁 Struktur File .env

### Backend (.env)
Located at: `backend/.env`
```env
GEMINI_API_KEY=AIzaSyBIh8y9NibKTSKMvL2FpoxMPo2sWYCIOVk
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent
```

### Frontend (.env)
Located at: `frontend/.env`
```env
VITE_API_URL=http://localhost:8000
```

### ML (.env)
Located at: `ml/.env`
```env
API_KEY_GEMINI=AIzaSyBIh8y9NibKTSKMvL2FpoxMPo2sWYCIOVk
API_KEY_DEEPSEEK=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
API_KEY_OCR=K81288052388957
API_KEY_BERT=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
```

## 🔄 Alur Kerja Aplikasi

### User Journey Flow

1. **User membuka browser** → `http://localhost:5173`
2. **Landing Page** - User dapat:
   - Upload file `.txt`
   - Drag & drop file
   - Paste teks langsung (Ctrl+V)
   - Paste URL berita
3. **Frontend mengirim data** → Backend API (`http://localhost:8000/api.php`)
4. **Backend memproses**:
   - Ekstrak teks dari file (jika file)
   - Kirim ke Gemini AI untuk analisis sentimen
   - Hitung Flesch Reading Ease untuk readability
   - Return JSON response
5. **Frontend menerima response** → Simpan di Pinia store
6. **Navigate ke Analysis Page** - Menampilkan:
   - Skor sentimen (Positive/Negative/Neutral)
   - Persentase sentimen
   - Skor readability (0-100)
   - Kategori keterbacaan
   - Jumlah kata & kalimat
   - Detail analisis dari AI

### API Communication

```
┌─────────────┐         POST /api.php          ┌─────────────┐
│             │  (text or file)                │             │
│  Frontend   ├───────────────────────────────>│   Backend   │
│  (Vue.js)   │                                │   (PHP)     │
│             │<───────────────────────────────┤             │
│             │    JSON Response               │             │
└─────────────┘                                └──────┬──────┘
                                                      │
                                                      │ Call API
                                                      ▼
                                              ┌───────────────┐
                                              │  Gemini API   │
                                              │ (Google AI)   │
                                              └───────────────┘
```

## 🎯 Fitur Utama

### Frontend Features
- ✅ Drag & Drop file upload
- ✅ Paste file/text/URL support
- ✅ Real-time API communication
- ✅ Responsive design
- ✅ Loading states
- ✅ Error handling
- ✅ Tab switching (Sentiment/Readability)
- ✅ Dynamic data visualization

### Backend Features
- ✅ RESTful API endpoint
- ✅ File upload support (.txt)
- ✅ Text input support (JSON)
- ✅ Gemini AI integration
- ✅ Flesch Reading Ease algorithm
- ✅ Fallback keyword-based sentiment
- ✅ CORS enabled
- ✅ Input validation

### ML Scripts Features
- ✅ Multiple AI service comparison
- ✅ Gemini 2.0 Flash
- ✅ DeepSeek Chat
- ✅ HuggingFace BERT (Multilingual)
- ✅ OCR support (images → text)
- ✅ HTML parsing
- ✅ CSV output

## 🧪 Testing

### Test Backend API

**1. Test dengan cURL (Windows PowerShell):**
```powershell
$body = @{text = "Presiden memberikan bantuan kepada rakyat"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api.php" -Method POST -Body $body -ContentType "application/json"
```

**2. Test dengan cURL (Windows CMD/Git Bash):**
```bash
curl -X POST http://localhost:8000/api.php ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"Berita positif hari ini\"}"
```

**3. Test File Upload:**
```bash
curl -X POST http://localhost:8000/api.php ^
  -F "file=@berita.txt"
```

### Test Frontend

1. Buka browser: `http://localhost:5173`
2. Upload file atau paste teks
3. Lihat hasil analisis di halaman `/analyze`
4. Check browser console untuk errors
5. Check Network tab untuk API calls

### Test ML Scripts

```bash
cd ml

# Test Gemini API
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Gemini API Key:', 'OK' if os.getenv('API_KEY_GEMINI') else 'NOT FOUND')"

# Test full analysis
python PBKK_script_api.py berita.html
```

## 🐛 Troubleshooting

### Backend tidak bisa diakses
```bash
# Pastikan port 8000 tidak digunakan
netstat -ano | findstr :8000

# Coba port lain
php -S localhost:8080
# Update frontend/.env: VITE_API_URL=http://localhost:8080
```

### CORS Error
- Pastikan backend sudah menjalankan `header('Access-Control-Allow-Origin: *');`
- File: `backend/public/api.php` line 9

### API Key Invalid
- Check file `.env` di folder backend dan ml
- Pastikan tidak ada spasi atau quote berlebih
- Format: `API_KEY_GEMINI=your_key_here` (tanpa quotes)

### Frontend tidak connect ke backend
- Check `frontend/.env` → `VITE_API_URL=http://localhost:8000`
- Restart frontend dev server setelah ubah .env
- Check browser console untuk error messages

### Python ModuleNotFoundError
```bash
pip install requests beautifulsoup4 python-dotenv
```

## 📊 Contoh Output

### Backend API Response
```json
{
  "success": true,
  "text": "Presiden memberikan bantuan kepada rakyat yang membutuhkan. Program ini sangat membantu masyarakat.",
  "sentiment": "Positive",
  "sentiment_score": 0.75,
  "sentiment_details": "Sentimen: Positif, Alasan: Terdapat kata-kata positif seperti 'bantuan', 'membantu', dan 'baik'.",
  "readability": 72.5,
  "readability_category": "Cukup Mudah",
  "word_count": 15,
  "sentence_count": 2
}
```

### ML Script Output (Console)
```
Loaded API keys:
 - GEMINI: yes
 - DEEPSEEK: yes
 - BERT: yes

Analyzing text with Gemini...
✓ Sentiment: Positive (Score: 0.78)
✓ Details: Berita ini positif karena...

Analyzing text with DeepSeek...
✓ Sentiment: Positive (Score: 0.72)

Analyzing text with BERT...
✓ Sentiment: 4/5 stars (Positive)

Results saved to: api_comparison_results.csv
```

## 🚢 Deployment (Production)

### Backend
1. Upload folder `backend` ke server (XAMPP/Apache/Nginx)
2. Set document root ke `backend/public`
3. Update `backend/.env` dengan production API keys
4. Enable HTTPS
5. Restrict CORS di `api.php` untuk domain spesifik

### Frontend
```bash
cd frontend
npm run build
# Upload folder dist/ ke hosting
# Configure web server untuk SPA routing
```

### Nginx Config (SPA)
```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

## 📝 Notes

- API Gemini free tier memiliki rate limit (15 requests per minute)
- File upload saat ini hanya support `.txt` (PDF & DOCX coming soon)
- Readability score menggunakan algoritma Flesch Reading Ease (bahasa Indonesia)
- ML scripts bisa dijalankan independent dari web app

## 🔗 Endpoints

| Service | URL | Method | Description |
|---------|-----|--------|-------------|
| Frontend | `http://localhost:5173` | GET | Landing page |
| Frontend | `http://localhost:5173/analyze` | GET | Analysis results |
| Backend API | `http://localhost:8000/api.php` | POST | Analyze text/file |

## 💡 Tips

1. **Development**: Jalankan backend dan frontend secara bersamaan di 2 terminal berbeda
2. **Testing**: Gunakan file `ml/berita.txt` atau `ml/berita.html` untuk test
3. **Debugging**: Check browser DevTools Console dan Network tab
4. **API Errors**: Lihat response dari backend di Network tab untuk detail error

## ✅ Checklist Sebelum Deploy

- [ ] Backend berjalan di `http://localhost:8000`
- [ ] Frontend berjalan di `http://localhost:5173`
- [ ] API keys valid dan tersimpan di `.env` files
- [ ] CORS enabled di backend
- [ ] Test upload file .txt
- [ ] Test paste text
- [ ] Hasil analisis muncul di Analysis Page
- [ ] Tab switching (Sentiment/Readability) berfungsi
- [ ] ML scripts bisa load API keys dari .env
- [ ] Error handling berfungsi dengan baik

---

**Created**: 2025
**Version**: 1.0.0
**Status**: Fully Integrated & Ready to Use

Jika ada pertanyaan atau masalah, silakan check dokumentasi API atau hubungi developer.
