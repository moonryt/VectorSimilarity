<script setup lang="ts">
import dayjs from "dayjs"
import {computed, onMounted, ref} from "vue"
import { useHead } from "@unhead/vue"
import { useRoute } from "vue-router"
import {ArrowLeft, Clock3, Info, Scale, Tangent, Brain, SquareFunction} from "lucide-vue-next"
import router from "@/router"
import { useVectorHistoryStore } from "@/stores/vectorHistory"
import AlgorithmDetail from "@/components/AlgorithmDetail.vue";

const route = useRoute()
const historyStore = useVectorHistoryStore()

const recordId = computed(() => {
  const id = route.params.id
  return Array.isArray(id) ? id[0] : id
})

const record = computed(() => (recordId.value ? historyStore.findRecord(recordId.value) : undefined))

useHead({
  title: computed(() => {
    if (!record.value) {
      return "对比结果"
    }

    return `${shortText(record.value.response.texts.text1)} vs ${shortText(record.value.response.texts.text2)}`
  }),
  meta: [
    {
      name: "description",
      content: "查看本次文本近似度、语义相似度、余弦值结果。",
    },
  ],
})

function shortText(value: string) {
  const chars = Array.from(value)
  return chars.length > 10 ? `${chars.slice(0, 10).join("")}...` : value
}

function handleBack() {
  if (window.history.state?.back) {
    router.back()
    return
  }

  void router.replace("/")
}

const cosineFormula = String.raw`\cos\theta`
</script>

<template>
  <div class="space-y-0">
    <n-card size="small" class="border-b-0!">
      <template #header>
        <div class="flex h-7 w-full items-center gap-3">
          <n-button quaternary circle size="small" @click="handleBack">
            <template #icon>
              <n-icon><ArrowLeft /></n-icon>
            </template>
          </n-button>
          <n-icon><Scale /></n-icon>
          <span>对比结果</span>
        </div>
      </template>

    </n-card>

    <n-card class="border-b-0!">
      <n-empty v-if="!record" description="没有找到这条对比记录">
        <template #extra>
          <n-button type="primary" @click="router.push('/compare')">重新对比</n-button>
        </template>
      </n-empty>

      <div v-else class="space-y-0">
        <h2 class="text-2xl leading-snug">
          「{{ shortText(record.response.texts.text1) }}」与「{{ shortText(record.response.texts.text2) }}」
        </h2>

        <h1 class="text-4xl font-bold leading-tight pt-1">
          近似度为
          <n-number-animation
            :from="0.00"
            :to="record.response.adjustedValue"
            :precision="2"
            :duration="1300"
          />
          %
        </h1>

        <div class="items-center opacity-85 pt-1.5">
          语义相似度
          <n-number-animation
            :from="0.00"
            :to="record.response.percentValue"
            :precision="2"
            :duration="1400"
          />
          %
        </div>

        <p class="text-sm opacity-80 pt-3 pb-1">
          近似度和语义相似度反应了这两个文段意思上的相似度，而非只看字是否相同。它们的相似度也人工直接赋予，而是基于 AI 与算法。
        </p>
      </div>
    </n-card>

    <n-card v-if="record" class="border-b-0!">
      <template #header>
        <div class="flex items-center gap-2">
          <n-icon><Info /></n-icon>
          <span>计算信息</span>
        </div>
      </template>

      <div class="grid gap-4">
        <div>
          <div class="mb-2 flex items-center gap-2 text-sm opacity-75">
            <n-icon><Clock3 /></n-icon>
            <span>完成时间</span>
          </div>
          <div class="text-base">
            {{ dayjs(record.completedAt).format("YYYY年MM月DD日 HH:mm") }}
          </div>
        </div>

        <div>
          <div class="mb-2 flex items-center gap-2 text-sm opacity-75">
            <n-icon><Tangent /></n-icon>
            <span>实际夹角余弦值</span>
          </div>
          <div class="text-base">
            <n-equation :value="cosineFormula" />
            =
            {{ record.response.cosineFullPrecision.substring(0, 13) }}
          </div>
        </div>

        <div>
          <div class="mb-2 flex items-center gap-2 text-sm opacity-75">
            <n-icon><Brain /></n-icon>
            <span>AI 嵌入模型</span>
          </div>
          <div class="text-base">
            {{ record.response.model }}
          </div>
        </div>

      </div>
    </n-card>

    <n-card size="small" class="border-b-0!">
      <template #header>
        <div class="flex items-center gap-2">
          <n-icon><SquareFunction /></n-icon>
          <span>算法原理</span>
        </div>
      </template>


    </n-card>

    <AlgorithmDetail />

    <n-card size="small" class="border-b-0! flex items-center justify-center">
      <p>包含算法的更多信息请查看 <RouterLink to="/about" class="text-green">关于算法</RouterLink>。</p>
    </n-card>

  </div>
</template>
