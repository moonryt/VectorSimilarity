import { computed, ref } from "vue"
import { defineStore } from "pinia"

const MAX_HISTORY_RECORDS = 100

function createHistoryId() {
  if (crypto.randomUUID) {
    return crypto.randomUUID().replaceAll("-", "").slice(0, 12)
  }

  return `${Date.now().toString(36)}${Math.random().toString(36).slice(2, 8)}`
}

export const useVectorHistoryStore = defineStore(
  "vectorHistory",
  () => {
    const records = ref<Item.CompareHistoryRecord[]>([])

    const latestRecords = computed(() => records.value.slice().reverse())
    const recentFiveRecords = computed(() => latestRecords.value.slice(0, 5))

    function addRecord(request: Item.SimilarityRequest, response: Item.SimilarityResponse) {
      const id = response.id || createHistoryId()
      const completedAt = response.completedAt || new Date().toISOString()

      records.value.push({
        id,
        completedAt,
        request,
        response: {
          ...response,
          id,
          completedAt,
        },
      })

      if (records.value.length > MAX_HISTORY_RECORDS) {
        records.value.splice(0, records.value.length - MAX_HISTORY_RECORDS)
      }

      return id
    }

    function findRecord(id: string) {
      return records.value.find((record) => record.id === id)
    }

    function removeRecord(id: string) {
      records.value = records.value.filter((record) => record.id !== id)
    }

    function clearRecords() {
      records.value = []
    }

    return {
      records,
      latestRecords,
      recentFiveRecords,
      addRecord,
      findRecord,
      removeRecord,
      clearRecords,
    }
  },
  {
    persist: {
      key: "vector-compare-history",
    },
  },
)
