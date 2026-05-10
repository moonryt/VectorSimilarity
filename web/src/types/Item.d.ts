declare namespace Item {
  interface SimilarityRequest {
    text1: string
    text2: string
  }

  interface SanitizedTexts {
    text1: string
    text2: string
  }

  interface SimilarityResponse {
    id: string
    completedAt: string
    cosine: number
    cosineFullPrecision: string
    percent: string
    percentValue: number
    adjustedPercent: string
    adjustedValue: number
    model: string
    texts: SanitizedTexts
  }

  interface HealthResponse {
    status: string
    embeddingModel: string
  }

  interface CompareHistoryRecord {
    id: string
    completedAt: string
    request: SimilarityRequest
    response: SimilarityResponse
  }
}
