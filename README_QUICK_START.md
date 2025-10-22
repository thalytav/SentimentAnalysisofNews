# Quick Start Guide 🚀

Panduan cepat untuk menjalankan aplikasi Sentiment & Readability Analysis.

## ⚡ Cara Tercepat (Windows)

### Menggunakan Batch Files

**1. Start Backend:**
```
Double-click: start-backend.bat
```
Backend akan berjalan di `http://localhost:8000`

**2. Start Frontend (terminal baru):**
```
Double-click: start-frontend.bat
```
Frontend akan berjalan di `http://localhost:5173`

**3. Buka Browser:**
```
http://localhost:5173
```

## 📋 Manual Start

### Backend (Terminal 1)
```bash
cd Sentiment-ReadAbility-Analysis-of-News-Website-main/backend/public
php -S localhost:8000
```

### Frontend (Terminal 2)
```bash
cd Sentiment-ReadAbility-Analysis-of-News-Website-main/frontend
npm install  # Hanya pertama kali
npm run dev
```

### ML Scripts (Optional)
```bash
cd Sentiment-ReadAbility-Analysis-of-News-Website-main/ml
pip install requests beautifulsoup4 python-dotenv
python PBKK_script_api.py berita.html
```

## ✅ Test Cepat

### Test Backend API (PowerShell):
```powershell
$body = @{text = "Berita positif hari ini"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api.php" -Method POST -Body $body -ContentType "application/json"
```

### Test Frontend:
1. Buka `http://localhost:5173`
2. Paste teks: "Presiden memberikan bantuan kepada rakyat"
3. Tekan Ctrl+V
4. Lihat hasil analisis

## 🔑 API Keys (Sudah Dikonfigurasi)

✅ Semua API keys sudah tersimpan di file `.env`:
- Backend: `backend/.env`
- Frontend: `frontend/.env`
- ML: `ml/.env`

Tidak perlu setup lagi!

## 📊 Fitur yang Bisa Dicoba

1. **Upload File** - Upload file `.txt` berisi berita
2. **Paste Text** - Ctrl+V untuk paste teks langsung
3. **Paste URL** - Paste URL berita (akan di-fetch)
4. **Drag & Drop** - Drag file ke halaman
5. **Tab Switching** - Switch antara Sentiment dan Readability
6. **Real-time Analysis** - Hasil langsung dari AI (Gemini)

## 🐛 Troubleshooting

**Port sudah digunakan?**
```bash
# Ganti port backend
php -S localhost:8080

# Update frontend/.env
VITE_API_URL=http://localhost:8080
```

**Frontend tidak connect?**
- Pastikan backend sudah jalan di port 8000
- Check browser console (F12) untuk error
- Restart frontend setelah ubah .env

**Module not found (Python)?**
```bash
pip install requests beautifulsoup4 python-dotenv
```

## 📖 Dokumentasi Lengkap

Lihat: [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)

## 🎯 Expected Results

### Sentiment Analysis
- **Positive**: "Presiden memberikan bantuan kepada rakyat"
- **Negative**: "Korupsi merajalela dan ekonomi memburuk"
- **Neutral**: "Presiden menghadiri rapat kabinet hari ini"

### Readability Score
- **90-100**: Sangat Mudah
- **80-89**: Mudah
- **70-79**: Cukup Mudah
- **60-69**: Standar
- **50-59**: Cukup Sulit
- **30-49**: Sulit
- **0-29**: Sangat Sulit

---

**Total Setup Time**: ~2 menit
**Created**: 2025
**Status**: Ready to Use ✅
