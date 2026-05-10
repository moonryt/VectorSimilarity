import http from "@/axios"

export function getVectorHealth() {
  return http.get<Item.HealthResponse>("/health").then((response) => response.data)
}

export async function compareSimilarity(payload: Item.SimilarityRequest) {
  const response = await http
    .post<Item.SimilarityResponse>("/similarity", payload)
  return response.data
}
