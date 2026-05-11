<script setup lang="ts">
import { computed, onBeforeUnmount, reactive, ref, watch } from "vue"
import { useHead } from "@unhead/vue"
import { ArrowLeft, Eraser, History, LoaderCircle, Scale } from "lucide-vue-next"
import { compareSimilarity } from "@/apis/vector"
import router from "@/router"
import { useVectorHistoryStore } from "@/stores/vectorHistory"

const MAX_TEXT_LENGTH = 128
const FORMULA_INTERVAL_MS = 1250
const FADE_MS = 200
const RESULT_DELAY_MS = 500

const formulas = [
  String.raw`\cos\theta=\frac{\mathbf{a}\cdot\mathbf{b}}{|\mathbf{a}|\cdot|\mathbf{b}|}`,
  String.raw`n=\frac{\cos\theta+1}{2}`,
  String.raw`\sigma(n)=\frac{1}{1+e^{-8(n-0.65)}}`,
  String.raw`\operatorname{approx}(\mathbf{a},\mathbf{b})=100\cdot\sigma(n)^{0.8}`,
]

const historyStore = useVectorHistoryStore()

const form = reactive<Item.SimilarityRequest>({
  text1: "",
  text2: "",
})

const submitting = ref(false)
const submitAttempted = ref(false)
const text1Touched = ref(false)
const text2Touched = ref(false)
const formulaIndex = ref(0)
const formulaFading = ref(false)
let formulaTimer: number | undefined

useHead({
  title: "近似计算",
  meta: [
    {
      name: "description",
      content: "词相思，输入两个词汇或文本，计算它们的近似度和语义相似度。",
    },
  ],
})

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

function delay(ms: number) {
  return new Promise((resolve) => window.setTimeout(resolve, ms))
}

function handleClear() {
  form.text1 = ""
  form.text2 = ""
  submitAttempted.value = false
  text1Touched.value = false
  text2Touched.value = false
  formulaIndex.value = 0
  formulaFading.value = false
}

const text1Error = computed(() => getInputError(form.text1))
const text2Error = computed(() => getInputError(form.text2))

const visibleText1Error = computed(() =>
  text1Touched.value || submitAttempted.value ? text1Error.value : "",
)
const visibleText2Error = computed(() =>
  text2Touched.value || submitAttempted.value ? text2Error.value : "",
)
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
  submitAttempted.value = true

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
    await delay(RESULT_DELAY_MS)
    submitting.value = false
    void router.push(`/compare/result/${id}`)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <n-card size="small" class="border-b-0!">
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

    <div v-if="!submitting" class="flex px-2 text-sm">
      请输入两个想要查看其近似度的词汇或文本。
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
        label="第一个文本"
        :feedback="visibleText1Error || `${getTextLength(form.text1)} / ${MAX_TEXT_LENGTH - 1}`"
        :validation-status="visibleText1Error ? 'error' : undefined"
      >
        <n-input
          v-model:value="form.text1"
          clearable
          :disabled="submitting"
          placeholder="请输入第一个文本"
          @blur="text1Touched = true"
          @keyup.enter="handleSubmit"
        />
      </n-form-item>

      <n-form-item
        label="第二个文本"
        :feedback="visibleText2Error || `${getTextLength(form.text2)} / ${MAX_TEXT_LENGTH - 1}`"
        :validation-status="visibleText2Error ? 'error' : undefined"
      >
        <n-input
          v-model:value="form.text2"
          clearable
          :disabled="submitting"
          placeholder="请输入第二个文本"
          @blur="text2Touched = true"
          @keyup.enter="handleSubmit"
        />
      </n-form-item>
    </div>

    <div class="flex justify-end gap-2">
      <n-button secondary :disabled="submitting" @click="handleClear">
        <template #icon>
          <n-icon><Eraser /></n-icon>
        </template>
        清空
      </n-button>

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
