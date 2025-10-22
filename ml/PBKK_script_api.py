import requests
import json
import os
import sys
import argparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
# Pastikan Anda punya file ocr_utils.py atau hapus/sesuaikan impor ini
from ocr_utils import extract_text_from_image

# Load API keys dari file .env
# Pertama coba load dari CWD; jika kunci tidak ditemukan, coba load dari folder skrip (ml/).
load_dotenv()
script_dir = os.path.dirname(__file__)

# Jika beberapa key masih kosong, coba load .env yang ada di folder skrip
if not all([os.getenv("API_KEY_GEMINI"), os.getenv("API_KEY_DEEPSEEK"), os.getenv("API_KEY_BERT")]):
    env_path = os.path.join(script_dir, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path, override=False)

API_KEY_GEMINI = os.getenv("API_KEY_GEMINI")
API_KEY_DEEPSEEK = os.getenv("API_KEY_DEEPSEEK")
API_KEY_BERT = os.getenv("API_KEY_BERT")

# Print status singkat (tanpa mengekspos nilai penuh) agar mudah debug
def _mask(k):
    if not k:
        return None
    if len(k) <= 8:
        return k[:2] + '...' + k[-2:]
    return k[:4] + '...' + k[-4:]

print("Loaded API keys:")
print(f" - GEMINI: {'yes' if API_KEY_GEMINI else 'no'}")
print(f" - DEEPSEEK: {'yes' if API_KEY_DEEPSEEK else 'no'}")
print(f" - BERT: {'yes' if API_KEY_BERT else 'no'}")

# Endpoint untuk setiap API
ENDPOINT_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
ENDPOINT_DEEPSEEK = "https://openrouter.ai/api/v1/chat/completions"
ENDPOINT_BERT = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"


def normalize_api_result(api_service, result):
    """Extract a readable string from various API response shapes.

    Returns a string summary or None if nothing could be extracted.
    """
    if not result:
        return None

    try:
        if api_service == "gemini":
            # Gemini responses commonly have: {"candidates": [{"content": {"parts": [{"text": ...}]}}]}
            if isinstance(result, dict):
                cand = result.get("candidates")
                if isinstance(cand, list) and cand:
                    parts_texts = []
                    for c in cand:
                        content = c.get("content", {})
                        parts = content.get("parts", []) if isinstance(content, dict) else []
                        for p in parts:
                            if isinstance(p, dict) and p.get("text"):
                                parts_texts.append(p.get("text"))
                    if parts_texts:
                        return "\n\n".join(parts_texts)
            # fallback
            return json.dumps(result, indent=2, ensure_ascii=False)

        if api_service == "deepseek":
            # Try common chat completion shapes: {choices: [{message: {content: ...}}]}
            if isinstance(result, dict):
                choices = result.get("choices")
                if isinstance(choices, list) and choices:
                    texts = []
                    for ch in choices:
                        msg = ch.get("message") or ch.get("text") or ch.get("content")
                        if isinstance(msg, dict):
                            texts.append(msg.get("content") or json.dumps(msg, ensure_ascii=False))
                        elif isinstance(msg, str):
                            texts.append(msg)
                    if texts:
                        return "\n\n".join(texts)
            return json.dumps(result, indent=2, ensure_ascii=False)

        if api_service == "bert":
            # HuggingFace inference often returns a list of {label, score}
            if isinstance(result, list):
                labels = []
                for item in result:
                    if isinstance(item, dict):
                        label = item.get("label") or item.get("class")
                        score = item.get("score")
                        if label is not None and score is not None:
                            labels.append(f"{label} ({score:.3f})")
                if labels:
                    return ", ".join(labels)
            return json.dumps(result, indent=2, ensure_ascii=False)

        # default fallback
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception:
        return json.dumps(result, indent=2, ensure_ascii=False)

def clean_html_text(html_text):
    """Menghapus tag HTML dari teks."""
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def get_api_config(api_service):
    """Mengambil konfigurasi API berdasarkan nama layanan."""
    # Pastikan API Keys sudah terisi, jika tidak beri peringatan
    if not all([API_KEY_GEMINI, API_KEY_DEEPSEEK, API_KEY_BERT]):
        print("PERINGATAN: Tidak semua API Key ditemukan di file .env. Pastikan variabel API_KEY_GEMINI, API_KEY_DEEPSEEK, dan API_KEY_BERT sudah diatur.")

    config = {
        "gemini": {
            "key": API_KEY_GEMINI,
            "url": ENDPOINT_GEMINI,
            "payload_template": lambda text: {
                "contents": [{"parts": [{"text": f"Analisis sentimen dari teks berikut: '{text}'. Apakah sentimennya positif, negatif, atau netral? Berikan alasannya dan highlight kata-kata penyebabnya."}]}]
            }
        },
        "deepseek": {
            "key": API_KEY_DEEPSEEK,
            "url": ENDPOINT_DEEPSEEK,
            "payload_template": lambda text: {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": f"Analisis sentimen dari teks berikut: '{text}'. Tentukan apakah sentimennya positif, negatif, atau netral. Berikan alasannya dan highlight kata-kata yang relevan."}]
            },
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY_DEEPSEEK}"
            }
        },
        "bert": {
            "key": API_KEY_BERT,
            "url": ENDPOINT_BERT,
            "payload_template": lambda text: {"inputs": text},
            "headers": {"Authorization": f"Bearer {API_KEY_BERT}"}
        }
    }
    return config.get(api_service)

def analyze_text_directly(text, api_service="gemini"):
    """Langsung analisis teks tanpa perlu file."""
    api_config = get_api_config(api_service)
    if not api_config or not api_config.get("key"):
        msg = f"Konfigurasi atau API Key untuk {api_service} tidak ditemukan. Melewati..."
        print(msg)
        return {"_error": msg}

    payload = api_config["payload_template"](text)
    headers = api_config.get("headers", {})
    
    try:
        if api_service in ["deepseek", "bert"]:
            # Timeout dinaikkan menjadi 60 detik
            print(f"Menghubungi {api_service.upper()}... (mungkin butuh waktu jika model sedang 'tidur')")
            response = requests.post(api_config["url"], headers=headers, json=payload, timeout=60)
        else: # Gemini
            print(f"Menghubungi {api_service.upper()}...")
            response = requests.post(f"{api_config['url']}?key={api_config['key']}", json=payload, timeout=60)

        # If response is not OK, include status code and a truncated body to help debugging
        if not response.ok:
            body = response.text or ''
            snippet = (body[:1000] + '...') if len(body) > 1000 else body
            msg = f"Error saat menghubungi API {api_service}: {response.status_code} - {snippet}"
            print(msg)
            return {"_error": msg}

        # OK
        return response.json()
    except requests.exceptions.RequestException as e:
        msg = f"Error saat menghubungi API {api_service}: {e}"
        print(msg)
        return {"_error": msg}

def analyze_news_from_html(file_path, api_service="gemini"):
    """Membaca file HTML dan analisis teksnya."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        plain_text = clean_html_text(html_content)
        if not plain_text:
            print("Error: Tidak ditemukan teks dalam file HTML.")
            return None
        return analyze_text_directly(plain_text, api_service)
    except FileNotFoundError:
        msg = f"Error: File '{file_path}' tidak ditemukan."
        print(msg)
        return {"_error": msg}

def analyze_input(file_path, api_service):
    """Menganalisis input berdasarkan tipe file untuk satu layanan API."""
    # Resolve the input path: support absolute paths, CWD relative paths,
    # and paths relative to this script's directory.
    def resolve_file_path(p):
        # If already absolute and exists, return it
        if os.path.isabs(p) and os.path.exists(p):
            return p

        # Check relative to script directory
        script_dir = os.path.dirname(__file__)
        candidate = os.path.join(script_dir, p)
        if os.path.exists(candidate):
            return candidate

        # Check as given relative to current working directory
        abs_candidate = os.path.abspath(p)
        if os.path.exists(abs_candidate):
            return abs_candidate

        # Not found; return original so callers/handlers can handle FileNotFound
        return p

    resolved = resolve_file_path(file_path)
    ext = os.path.splitext(resolved)[-1].lower()

    # If the resolved path does not exist, show helpful debug info and stop early
    if not os.path.exists(resolved):
        print(f"Error: File '{file_path}' tidak ditemukan.")
        print("Paths diperiksa:")
        print(f" - as given: {os.path.abspath(file_path)}")
        print(f" - relative to script: {os.path.join(os.path.dirname(__file__), file_path)}")
        print(f"Current working directory: {os.getcwd()}")
        return None

    if ext in [".html", ".htm"]:
        return analyze_news_from_html(resolved, api_service)
    elif ext in [".jpg", ".jpeg", ".png"]:
        print(f"Menjalankan OCR pada {resolved}...")
        extracted_text = extract_text_from_image(resolved)
        if not extracted_text:
            msg = "Gagal mengekstrak teks dari gambar."
            print(msg)
            return {"_error": msg}
        print("Teks hasil OCR berhasil diekstrak. Mengirim ke API analisis...")
        return analyze_text_directly(extracted_text, api_service)
    elif ext == ".txt":
        with open(resolved, "r", encoding="utf-8") as f:
            text = f.read()
        return analyze_text_directly(text, api_service)
    else:
        print(f"Format file '{ext}' tidak didukung.")
        msg = f"Format file '{ext}' tidak didukung."
        return {"_error": msg}

# --- FUNGSI BARU UNTUK MEMBANDINGKAN ---
def compare_all_services(file_path):
    """
    Memanggil semua layanan API (Gemini, DeepSeek, BERT) untuk menganalisis 
    satu file input dan mengembalikan semua hasilnya.
    """
    services = ["gemini", "deepseek", "bert"]
    all_results = {}

    print(f"Memulai analisis komparatif untuk file: '{file_path}'")
    
    for service in services:
        print("-" * 20)
        print(f"🚀 Memproses dengan layanan: {service.upper()}")
        result = analyze_input(file_path, api_service=service)
        if not result:
            all_results[service] = "Gagal mendapatkan hasil."
        elif isinstance(result, dict) and result.get("_error"):
            all_results[service] = f"ERROR: {result.get('_error')}"
        else:
            # try to normalize into readable text
            normalized = normalize_api_result(service, result)
            all_results[service] = normalized if normalized else (json.dumps(result, indent=2, ensure_ascii=False))
    
    print("-" * 20)
    print("Analisis komparatif selesai.")
    return all_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisis sentimen: file input (html, txt, atau gambar).")
    parser.add_argument("file", nargs="?", default="berita.png", help="Path ke file (default: berita.png)")
    args = parser.parse_args()

    file_input = args.file

    # Memanggil fungsi pembanding baru
    hasil_komparasi = compare_all_services(file_input)

    # Mencetak hasil gabungan dengan format yang rapi
    if hasil_komparasi:
        print("\n" + "="*50)
        print("HASIL ANALISIS KOMPARATIF")
        print("="*50)
        print(json.dumps(hasil_komparasi, indent=4, ensure_ascii=False))

