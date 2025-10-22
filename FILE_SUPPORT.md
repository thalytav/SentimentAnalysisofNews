# File Format Support

## ✅ Format yang Didukung Saat Ini

### `.txt` - Plain Text Files
- **Status**: ✅ Fully Supported
- **Cara Upload**: Klik "Upload Document" atau drag & drop
- **Max Size**: 10 MB (default PHP limit)
- **Encoding**: UTF-8 recommended

**Contoh penggunaan:**
1. Buat file `berita.txt` dengan Notepad
2. Isi dengan teks berita dalam bahasa Indonesia
3. Upload ke aplikasi
4. Lihat hasil analisis sentiment & readability

---

## ⏳ Format yang Akan Didukung

### `.pdf` - PDF Documents
- **Status**: ⏳ Coming Soon
- **Planned**: Extract text from PDF using PHP libraries
- **ETA**: Future update

### `.docx` - Microsoft Word Documents
- **Status**: ⏳ Coming Soon
- **Planned**: Extract text from DOCX using PHP libraries
- **ETA**: Future update

---

## 🎯 Alternatif: Paste Text Langsung

Jika file Anda bukan `.txt`, gunakan fitur **Paste Text**:

### Cara 1: Copy-Paste Manual
1. Buka file PDF/DOCX/lainnya
2. Select All (Ctrl+A) → Copy (Ctrl+C)
3. Di landing page, Paste (Ctrl+V)
4. Teks akan langsung dianalisis

### Cara 2: Paste URL
1. Copy URL artikel berita
2. Di landing page, Paste (Ctrl+V)
3. Aplikasi akan fetch content dari URL

---

## 🛠️ Technical Details

### Validasi Frontend (LandingPage.vue)
```typescript
const allowedExtensions = ['.txt']
const fileName = file.name.toLowerCase()
const isValidFile = allowedExtensions.some(ext => fileName.endsWith(ext))
```

### Validasi Backend (api.php)
```php
$extension = pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION);
if ($extension === 'txt') {
    $text = file_get_contents($filePath);
} else {
    http_response_code(400);
    echo json_encode(['error' => 'Only .txt files supported']);
}
```

---

## ❓ FAQ

**Q: Kenapa hanya `.txt` yang didukung?**
A: Untuk MVP (Minimum Viable Product), `.txt` paling mudah di-handle. PDF dan DOCX memerlukan library tambahan untuk extract text.

**Q: Kapan PDF/DOCX akan didukung?**
A: Akan ditambahkan di update berikutnya. Saat ini fokus pada core functionality (sentiment & readability analysis).

**Q: Bagaimana jika saya punya file PDF?**
A: Gunakan fitur Paste Text. Buka PDF di reader, copy text, lalu paste di aplikasi.

**Q: Apakah ada batasan ukuran file?**
A: Default PHP limit adalah 2MB untuk upload. Bisa dinaikkan di `php.ini` dengan mengubah `upload_max_filesize`.

**Q: Apakah mendukung bahasa selain Indonesia?**
A: Backend menggunakan Gemini AI yang support multi-language, tapi dioptimalkan untuk bahasa Indonesia.

---

## 📊 Roadmap

- [x] Plain text (.txt)
- [ ] PDF documents (.pdf)
- [ ] Word documents (.docx)
- [ ] HTML parsing (advanced)
- [ ] Batch upload (multiple files)
- [ ] URL fetch & scraping

---

**Last Updated**: 2025-10-23
**Version**: 1.0.0
