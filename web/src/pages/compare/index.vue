<script setup lang="ts">
import { computed, onBeforeUnmount, reactive, ref, watch } from "vue"
import { ArrowLeft, History, LoaderCircle, Scale } from "lucide-vue-next"
import { compareSimilarity } from "@/apis/vector"
import router from "@/router"
import { useVectorHistoryStore } from "@/stores/vectorHistory"

const MAX_TEXT_LENGTH = 128
const FORMULA_INTERVAL_MS = 1300
const FADE_MS = 200

const formulas = [
  String.raw`\mathbf{a}\cdot\mathbf{b}=\lVert\mathbf{a}\rVert\lVert\mathbf{b}\rVert\cos\theta`,
  String.raw`\text{f(x)}=\frac{\text{cosine}+1.0}{2.0}`,
  String.raw`\text{sigmoid(x)}=\frac{1.0}{1.0 + e^{-8.0(\text{f(x)}-0.65)}}`,
  String.raw`(\text{sigmoid(x)}^{0.8}) \times 100.0`,
]

const historyStore = useVectorHistoryStore()

const form = reactive<Item.SimilarityRequest>({
  text1: "",
  text2: "",
})

const submitting = ref(false)
const formulaIndex = ref(0)
const formulaFading = ref(false)
let formulaTimer: number | undefined

function getTextLength(value: string) {
  return Array.from(value.trim()).length
}

function getInputError(value: string) {
  const length = getTextLength(value)

  if (length === 0) {
    return "文本不能为空"
  }

  if (length >= MAX_TEXT_LENGTH) {
    return `文本需少于 ${MAX_TEXT_LENGTH} 字`
  }

  return ""
}

function shortText(value: string) {
  const chars = Array.from(value)
  return chars.length > 5 ? `${chars.slice(0, 6).join("")}...` : value
}

function stopFormulaLoop() {
  if (formulaTimer) {
    window.clearInterval(formulaTimer)
    formulaTimer = undefined
  }
}

function startFormulaLoop() {
  stopFormulaLoop()
  formulaIndex.value = 0
  formulaFading.value = false

  formulaTimer = window.setInterval(() => {
    formulaFading.value = true
    window.setTimeout(() => {
      formulaIndex.value = (formulaIndex.value + 1) % formulas.length
      formulaFading.value = false
    }, FADE_MS)
  }, FORMULA_INTERVAL_MS)
}

const text1Error = computed(() => getInputError(form.text1))
const text2Error = computed(() => getInputError(form.text2))
const canSubmit = computed(() => !text1Error.value && !text2Error.value && !submitting.value)

watch(submitting, (value) => {
  if (value) {
    startFormulaLoop()
    return
  }

  stopFormulaLoop()
})

onBeforeUnmount(stopFormulaLoop)

async function handleSubmit() {
  if (!canSubmit.value) {
    window.$message.warning("请先检查两个输入文本")
    return
  }

  submitting.value = true

  const request = {
    text1: form.text1.trim(),
    text2: form.text2.trim(),
  }

  try {
    const response = await compareSimilarity(request)
    const id = historyStore.addRecord(request, response)
    await router.push(`/compare/result/${id}`)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <n-card class="border-b-0!">
    <template #header>
      <div class="flex h-7 w-full items-center gap-3">
        <n-button quaternary circle size="small" @click="router.push('/')">
          <template #icon>
            <n-icon><ArrowLeft /></n-icon>
          </template>
        </n-button>
        <n-icon><Scale /></n-icon>
        <span>文本对比</span>
      </div>
    </template>

  </n-card>

  <n-card size="small" embedded class="flex justify-center border-b-0!">

    <div v-if="!submitting" class="flex px-2 text-base">
      请输入想要查看近似度的词汇或文本。
    </div>

    <div v-else class="flex items-center gap-3">
      <n-spin size="small" />
      <span class="shrink-0">正在计算：</span>
      <div
        class="min-w-0 transition-opacity duration-200"
        :class="formulaFading ? 'opacity-20' : 'opacity-100'"
      >
        <n-equation :value="formulas[formulaIndex]" />
      </div>
    </div>
  </n-card>

  <n-card class="space-y-5 border-b-0!">
    <div class="grid gap-4 md:grid-cols-2">
      <n-form-item
        label="文本 A"
        :feedback="text1Error || `${getTextLength(form.text1)} / ${MAX_TEXT_LENGTH - 1}`"
        :validation-status="text1Error ? 'error' : undefined"
      >
        <n-input
          v-model:value="form.text1"
          clearable
          :disabled="submitting"
          placeholder="请输入第一个文本"
          @keyup.enter="handleSubmit"
        />
      </n-form-item>

      <n-form-item
        label="文本 B"
        :feedback="text2Error || `${getTextLength(form.text2)} / ${MAX_TEXT_LENGTH - 1}`"
        :validation-status="text2Error ? 'error' : undefined"
      >
        <n-input
          v-model:value="form.text2"
          clearable
          :disabled="submitting"
          placeholder="请输入第二个文本"
          @keyup.enter="handleSubmit"
        />
      </n-form-item>
    </div>

    <div class="flex justify-end">
      <n-button type="primary" :loading="submitting" :disabled="!canSubmit" @click="handleSubmit">
        <template #icon>
          <n-icon>
            <LoaderCircle v-if="submitting" class="animate-spin" />
            <Scale v-else />
          </n-icon>
        </template>
        开始对比
      </n-button>
    </div>
  </n-card>

  <n-card size="small" class="border-b-0!">
    <template #header>
      <div class="flex items-center gap-2">
        <n-icon><History /></n-icon>
        <span>最近记录</span>
      </div>
    </template>

    <n-empty
      v-if="historyStore.recentFiveRecords.length === 0"
      size="small"
      description="暂无记录"
    />

    <n-list v-else hoverable clickable>
      <n-list-item
        v-for="record in historyStore.recentFiveRecords"
        :key="record.id"
        class="py-2!"
        @click="router.push(`/compare/result/${record.id}`)"
      >
        <div class="flex items-center justify-between gap-3">
          <n-ellipsis class="min-w-0">
            {{ shortText(record.request.text1) }} vs {{ shortText(record.request.text2) }}
          </n-ellipsis>
          <n-tag size="small" type="success">{{ record.response.adjustedPercent }}</n-tag>
        </div>
      </n-list-item>
    </n-list>
  </n-card>
</template>
