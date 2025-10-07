#sebelum memulai mari berdoa dan pip install requests beautifulsoup4 python-dotenv
#step 2 adalah membuat file .env di folder yang sama dengan try.py
#lalu masukkan API:
# API_KEY_GEMINI=your-gemini-api-key
# API_KEY_DEEPSEEK=your-deepseek-api-key
# API_KEY_BERT=your-huggingface-api-key (ini sikrit jadi jangan dishare)

import requests
import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load API keys dari file .env
load_dotenv()
API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")
API_KEY_DEEPSEEK = os.getenv("API_KEY_DEEPSEEK")
API_KEY_BERT = os.getenv("API_KEY_BERT")

# Endpoint untuk setiap API
ENDPOINT_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
ENDPOINT_DEEPSEEK = "https://openrouter.ai/api/v1/chat/completions"
ENDPOINT_BERT = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"

def clean_html_text(html_text):
    """Fungsi untuk menghapus tag HTML dari teks."""
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def get_api_config(api_service):
    """
    Memilih API key, endpoint, dan model berdasarkan nama layanan.
    """
    config = {
        "gemini": {
            "key": API_KEY_GEMINI,
            "url": ENDPOINT_GEMINI,
            "payload_template": lambda text: {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"Analisis sentimen dari berita berikut: '{text}'. "
                                        "Apakah sentimennya positif, negatif, atau netral? Berikan alasannya dan highlight kata-kata penyebabnya. "
                                        "Lalu, berikan juga analisis keterbacaan (readability) dari teks tersebut."
                            }
                        ]
                    }
                ]
            }
        },
        "deepseek": {
            "key": API_KEY_DEEPSEEK,
            "url": ENDPOINT_DEEPSEEK,
            "payload_template": lambda text: {
                "model": "deepseek/deepseek-chat-v3.1:free",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Analisis sentimen dan keterbacaan dari teks berikut: '{text}'."
                                   " Tentukan apakah sentimennya positif, negatif, atau netral. Berikan alasannya dan highlight kata-kata yang relevan."
                                   " Sertakan juga analisis keterbacaan (readability) dari teks tersebut."
                    }
                ]
            },
            "headers": { "Content-Type": "application/json", "Authorization": f"Bearer {API_KEY_DEEPSEEK}" }
        },
        "bert": {
            "key": API_KEY_BERT,
            "url": ENDPOINT_BERT,
            "payload_template": lambda text: { "inputs": text },
            "headers": { "Authorization": f"Bearer {API_KEY_BERT}" }
        }
    }
    return config.get(api_service)

def analyze_news_from_html(file_path, api_service="gemini"):
    """
    Fungsi untuk membaca file HTML, membersihkan teksnya,
    dan mengirimkannya ke API yang dipilih untuk dianalisis.
    """
    api_config = get_api_config(api_service)
    
    if not api_config:
        print(f"Error: Layanan API '{api_service}' tidak didukung.")
        return None

    api_key = api_config.get("key")
    api_url = api_config.get("url")
    payload_template = api_config.get("payload_template")
    headers = api_config.get("headers", {})

    if not api_key:
        print(f"Error: API key untuk {api_service} tidak ditemukan.")
        print("Pastikan Anda sudah mengatur file .env dengan benar.")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        plain_text = clean_html_text(html_content)
        
        if not plain_text:
            print("Error: Teks tidak ditemukan di dalam file HTML.")
            return None
        
        payload = payload_template(plain_text)
        
        # Kirim permintaan API
        if api_service in ["deepseek", "bert"]:
            response = requests.post(api_url, headers=headers, json=payload)
        else:
            response = requests.post(f"{api_url}?key={api_key}", json=payload)
            
        response.raise_for_status()
        
        return response.json()
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengirim permintaan ke {api_service}: {e}")
        return None

# ---

### Cara Menggunakan
# Untuk menguji API yang berbeda, Anda cukup memanggil fungsi `analyze_news_from_html()` dengan parameter `api_service` yang berbeda.

# ```python
# Proses File
nama_file_html = "berita.html"
print(f"Memproses file: {nama_file_html}")

# Analisis menggunakan Gemini
print("\n--- Analisis Menggunakan Gemini ---")
hasil_analisis_gemini = analyze_news_from_html(nama_file_html, api_service="gemini")
if hasil_analisis_gemini:
    print(json.dumps(hasil_analisis_gemini, indent=4))

# Analisis menggunakan DeepSeek
print("\n--- Analisis Menggunakan DeepSeek ---")
hasil_analisis_deepseek = analyze_news_from_html(nama_file_html, api_service="deepseek")
if hasil_analisis_deepseek:
    print(json.dumps(hasil_analisis_deepseek, indent=4))

# Analisis menggunakan BERT
print("\n--- Analisis Menggunakan BERT ---")
hasil_analisis_bert = analyze_news_from_html(nama_file_html, api_service="bert")
if hasil_analisis_bert:
    print(json.dumps(hasil_analisis_bert, indent=4))