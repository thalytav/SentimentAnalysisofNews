import requests
import json
import re
from bs4 import BeautifulSoup
from readability import Document
from dotenv import load_dotenv
import os

# ============================
# Load API Keys dari .env
# ============================
load_dotenv()
API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")
API_KEY_DEEPSEEK = os.getenv("API_KEY_DEEPSEEK")
API_KEY_BERT = os.getenv("API_KEY_BERT")

# ============================
# Endpoint Model
# ============================
ENDPOINT_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
ENDPOINT_DEEPSEEK = "https://openrouter.ai/api/v1/chat/completions"
ENDPOINT_BERT = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"


# ============================
# Fungsi: Ambil teks dari URL
# ============================
def fetch_article_text(url):
    """Ambil teks utama dari link berita"""
    print(f"🔗 Mengambil konten dari {url} ...")
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    html = resp.text
    doc = Document(html)
    article_html = doc.summary(html_partial=True)
    soup = BeautifulSoup(article_html, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ============================
# Fungsi: Analisis teks via API
# ============================
def analyze_text(text, api_service="gemini"):
    """Kirim teks ke layanan AI pilihan"""
    if api_service == "gemini":
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Analisis sentimen dari teks berikut: '{text}'. "
                                    f"Tentukan apakah positif, negatif, atau netral. Jelaskan alasannya."
                        }
                    ]
                }
            ]
        }
        response = requests.post(
            f"{ENDPOINT_GEMINI}?key={API_KEY_GEMINI}",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        return response.json()

    elif api_service == "deepseek":
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": f"Analisis sentimen dari teks berikut: '{text}'. "
                               f"Apakah positif, negatif, atau netral? Berikan alasan singkat."
                }
            ]
        }
        response = requests.post(
            ENDPOINT_DEEPSEEK,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY_DEEPSEEK}"
            },
            json=payload
        )
        return response.json()

    elif api_service == "bert":
        payload = {"inputs": text}
        response = requests.post(
            ENDPOINT_BERT,
            headers={"Authorization": f"Bearer {API_KEY_BERT}"},
            json=payload
        )
        return response.json()

    else:
        return {"_error": f"Layanan '{api_service}' tidak dikenali."}


# ============================
# Main Program
# ============================
if __name__ == "__main__":
    print("=" * 60)
    print("🧩  ANALISIS SENTIMEN DARI LINK BERITA  🧩")
    print("=" * 60)

    url = input("Masukkan link berita: ").strip()
    service = input("Pilih layanan (gemini / deepseek / bert): ").strip().lower()

    try:
        article_text = fetch_article_text(url)
        print(f"\n✅ Teks berhasil diambil ({len(article_text)} karakter pertama):")
        print(article_text[:300] + "...\n")

        print(f"🚀 Mengirim ke model {service.upper()} ...\n")
        result = analyze_text(article_text, api_service=service)

        print("=== HASIL ANALISIS ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
