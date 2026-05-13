<script setup lang="ts">
import dayjs from "dayjs"
import { computed, ref, watch } from "vue"
import { useHead } from "@unhead/vue"
import { useInfiniteScroll } from "@vueuse/core"
import { useRoute } from "vue-router"
import { ArrowLeft, Clock3, History, Trash2 } from "lucide-vue-next"
import router from "@/router"
import { useVectorHistoryStore } from "@/stores/vectorHistory"

const LOAD_STEP = 8

const historyStore = useVectorHistoryStore()
const route = useRoute()
const visibleCount = ref(LOAD_STEP)

const visibleRecords = computed(() => historyStore.latestRecords.slice(0, visibleCount.value))
const hasMoreRecords = computed(() => visibleCount.value < historyStore.latestRecords.length)

useHead({
  title: "历史记录",
  meta: [
    {
      name: "description",
      content: "查看本地的文本近似度对比历史。",
    },
  ],
})

function shortText(value: string) {
  const chars = Array.from(value)
  return chars.length > 5 ? `${chars.slice(0, 6).join("")}...` : value
}

function handleLoadMore() {
  if (!hasMoreRecords.value) {
    return
  }

  visibleCount.value = Math.min(
    visibleCount.value + LOAD_STEP,
    historyStore.latestRecords.length,
  )
}

function handleClearRecords() {
  historyStore.clearRecords()
  visibleCount.value = LOAD_STEP
}

function goResult(id: string) {
  void router.push(`/compare/result/${id}`)
}

useInfiniteScroll(window, handleLoadMore, {
  distance: 120,
  interval: 150,
  canLoadMore: () => route.path === "/history" && hasMoreRecords.value,
})

watch(
  () => historyStore.records.length,
  () => {
    if (visibleCount.value > historyStore.latestRecords.length) {
      visibleCount.value = Math.max(LOAD_STEP, historyStore.latestRecords.length)
    }
  },
)
</script>

<template>
  <n-card size="small" class="border-b-0!">
    <template #header>
      <div class="flex h-7 w-full items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <n-button quaternary circle size="small" @click="router.push('/')">
            <template #icon>
              <n-icon><ArrowLeft /></n-icon>
            </template>
          </n-button>
          <n-icon><History /></n-icon>
          <span>历史记录</span>
        </div>

        <n-button
          quaternary
          circle
          size="small"
          :disabled="historyStore.records.length === 0"
          @click="handleClearRecords"
        >
          <template #icon>
            <n-icon><Trash2 /></n-icon>
          </template>
        </n-button>
      </div>
    </template>

  </n-card>

  <n-card class="border-b-0!">
    <n-empty v-if="historyStore.records.length === 0" description="暂无历史记录" />

    <div v-else class="space-y-4">
      <div class="space-y-3">
        <n-card
          v-for="record in visibleRecords"
          :key="record.id"
          size="small"
          embedded
          class="cursor-pointer transition-colors"
          @click="goResult(record.id)"
        >
          <div class="flex items-center justify-between gap-3">
            <n-ellipsis class="min-w-0 text-base">
              {{ shortText(record.request.text1) }} 与 {{ shortText(record.request.text2) }}
            </n-ellipsis>
            <n-tag size="small" type="success">{{ record.response.adjustedPercent }}</n-tag>
          </div>

          <div class="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs opacity-70">
            <span class="flex items-center gap-1">
              <n-icon><Clock3 /></n-icon>
              {{ dayjs(record.completedAt).format("YYYY年MM月DD日 HH:mm") }}
            </span>
            <span>语义相似度 {{ record.response.percent }}</span>
          </div>
        </n-card>
      </div>

      <div v-if="hasMoreRecords" class="flex justify-center py-3">
        <n-button quaternary size="small" @click="handleLoadMore">
          继续浏览以加载更多
        </n-button>
      </div>

      <div v-else class="py-3 text-center text-xs opacity-60">
        已加载全部历史记录
      </div>
    </div>
  </n-card>
</template>
