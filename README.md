# Sentiment & ReadAbility Analysis of News Website

An AI-powered web application that allows users to upload or enter news text for automatic sentiment and readability analysis. The system uses Google Gemini AI to determine whether the news is positive, negative, or neutral, while calculating readability scores using the Flesch Reading Ease algorithm to assess how easy the content is to understand.

## ✨ Features

- **Sentiment Analysis** - Detect sentiment (Positive/Negative/Neutral) using Gemini AI
- **Readability Scoring** - Calculate Flesch Reading Ease score (0-100)
- **Multiple Input Methods** - Upload files, paste text, drag & drop, or paste URLs
- **Real-time Analysis** - Instant results powered by AI
- **Visual Dashboard** - Beautiful sentiment gauge and readability display
- **Tab Switching** - Switch between Sentiment and Readability views
- **ML Scripts** - Compare multiple AI services (Gemini, DeepSeek, BERT)

## 🚀 Quick Start

### Fastest Way (Windows)
1. Double-click `start-backend.bat`
2. Double-click `start-frontend.bat`
3. Open browser: `http://localhost:5173`

### Manual Start
```bash
# Terminal 1 - Backend
cd Sentiment-ReadAbility-Analysis-of-News-Website-main/backend/public
php -S localhost:8000

# Terminal 2 - Frontend
cd Sentiment-ReadAbility-Analysis-of-News-Website-main/frontend
npm install
npm run dev
```

See [README_QUICK_START.md](README_QUICK_START.md) for detailed instructions.

## 📚 Documentation

- **[Quick Start Guide](README_QUICK_START.md)** - Get started in 2 minutes
- **[Integration Guide](INTEGRATION_GUIDE.md)** - Complete setup & deployment guide
- **[Integration Summary](INTEGRATION_SUMMARY.md)** - Technical overview & changes

## 🛠️ Tech Stack

### Frontend
- Vue.js 3 (Composition API)
- TypeScript
- Vite
- Pinia (State Management)
- TailwindCSS

### Backend
- PHP 8.1+
- Laravel 10 Framework
- Google Gemini AI API
- Flesch Reading Ease Algorithm

### ML Scripts
- Python 3.10+
- Google Gemini API
- DeepSeek Chat API
- HuggingFace BERT
- OCR.Space API
- BeautifulSoup4

## 📊 How It Works

```
User Input → Frontend (Vue.js) → Backend API (PHP) → Gemini AI
                                                    ↓
                                           Sentiment Analysis
                                                    ↓
                                         Readability Calculation
                                                    ↓
                                    JSON Response → Display Results
```

## 🔑 API Keys

All API keys are pre-configured in `.env` files:
- ✅ Gemini AI (Sentiment Analysis)
- ✅ DeepSeek Chat (Alternative AI)
- ✅ HuggingFace BERT (Multilingual)
- ✅ OCR.Space (Image to Text)

## 🎯 Use Cases

- **Journalists** - Analyze news tone before publishing
- **Editors** - Check readability for target audience
- **Researchers** - Compare sentiment across multiple sources
- **Students** - Learn about NLP and sentiment analysis
- **Content Creators** - Optimize content readability

## 📁 Project Structure

```
Sentiment-ReadAbility-Analysis-of-News-Website-main/
├── frontend/          # Vue.js 3 application
├── backend/           # Laravel PHP API
├── ml/                # Python ML scripts
├── INTEGRATION_GUIDE.md
├── README_QUICK_START.md
├── start-backend.bat
└── start-frontend.bat
```

## ✅ Status

🟢 **Fully Integrated & Production Ready**

All components are connected and working:
- ✅ Backend API responding
- ✅ Frontend connected
- ✅ Gemini AI integrated
- ✅ ML scripts configured
- ✅ Documentation complete

## 🤝 Contributing

This project is for educational and research purposes. The system helps journalists, editors, and readers evaluate the quality of news content.
