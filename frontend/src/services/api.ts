// API Service untuk koneksi ke Backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface AnalysisResult {
  success: boolean
  text: string
  sentiment: string
  sentiment_score: number
  sentiment_details: string
  readability: number
  readability_category: string
  word_count: number
  sentence_count: number
  error?: string
}

/**
 * Mengirim teks untuk dianalisis
 */
export async function analyzeText(text: string): Promise<AnalysisResult> {
  try {
    const response = await fetch(`${API_BASE_URL}/api.php`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error analyzing text:', error)
    throw error
  }
}

/**
 * Mengirim file untuk dianalisis
 */
export async function analyzeFile(file: File): Promise<AnalysisResult> {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${API_BASE_URL}/api.php`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error analyzing file:', error)
    throw error
  }
}

/**
 * Mengambil teks dari URL dan menganalisisnya
 */
export async function analyzeUrl(url: string): Promise<AnalysisResult> {
  try {
    // Untuk implementasi sederhana, kita fetch URL di frontend
    // Dalam production, sebaiknya backend yang melakukan fetch
    const response = await fetch(url)
    const text = await response.text()

    return await analyzeText(text)
  } catch (error) {
    console.error('Error analyzing URL:', error)
    throw error
  }
}
