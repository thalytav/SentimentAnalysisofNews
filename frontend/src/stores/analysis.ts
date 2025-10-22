import { defineStore } from 'pinia'
import type { AnalysisResult } from '@/services/api'

interface AnalysisState {
  result: AnalysisResult | null
  loading: boolean
  error: string | null
}

export const useAnalysisStore = defineStore('analysis', {
  state: (): AnalysisState => ({
    result: null,
    loading: false,
    error: null,
  }),

  getters: {
    hasResult: (state) => state.result !== null,
    isPositive: (state) => state.result?.sentiment === 'Positive',
    isNegative: (state) => state.result?.sentiment === 'Negative',
    isNeutral: (state) => state.result?.sentiment === 'Neutral',

    // Hitung persentase sentimen
    sentimentPercentages: (state) => {
      if (!state.result) return { positive: 0, negative: 0, neutral: 0 }

      const score = state.result.sentiment_score

      // Konversi score (0-1) ke persentase
      if (state.result.sentiment === 'Positive') {
        return {
          positive: Math.round(score * 100),
          negative: Math.round((1 - score) * 50),
          neutral: Math.round((1 - score) * 50),
        }
      } else if (state.result.sentiment === 'Negative') {
        return {
          positive: Math.round((1 - score) * 50),
          negative: Math.round(score * 100),
          neutral: Math.round((1 - score) * 50),
        }
      } else {
        return {
          positive: 33,
          negative: 33,
          neutral: 34,
        }
      }
    },
  },

  actions: {
    setResult(result: AnalysisResult) {
      this.result = result
      this.error = null
    },

    setLoading(loading: boolean) {
      this.loading = loading
    },

    setError(error: string) {
      this.error = error
      this.loading = false
    },

    clearResult() {
      this.result = null
      this.error = null
      this.loading = false
    },
  },
})
