import requests
import os
from dotenv import load_dotenv

# Load API key dari file .env
load_dotenv()
API_KEY_OCR = os.getenv("API_KEY_OCR")
ENDPOINT_OCR = "https://api.ocr.space/parse/image"

def extract_text_from_image(image_path):
    """
    Mengekstraksi teks dari gambar menggunakan OCR.Space API.
    Mendukung format JPG, JPEG, dan PNG.
    """
    if not API_KEY_OCR:
        print("Error: API_KEY_OCR tidak ditemukan di .env")
        return None

    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                ENDPOINT_OCR,
                files={"file": image_file},
                data={
                    "apikey": API_KEY_OCR,
                    "language": "eng",
                    "OCREngine": 2
                }
            )
        response.raise_for_status()
        result = response.json()

        if result.get("IsErroredOnProcessing"):
            print("Error OCR:", result.get("ErrorMessage"))
            return None

        parsed_results = result.get("ParsedResults")
        if not parsed_results or not parsed_results[0].get("ParsedText"):
            print("Tidak ada teks yang terdeteksi dari gambar.")
            return None

        parsed_text = parsed_results[0]["ParsedText"]
        return parsed_text.strip()

    except FileNotFoundError:
        print(f"Error: File {image_path} tidak ditemukan.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error saat memanggil API OCR: {e}")
        return None
