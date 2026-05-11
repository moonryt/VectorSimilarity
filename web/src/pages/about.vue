<script setup lang="ts">

import AlgorithmDetail from "@/components/AlgorithmDetail.vue";
import {useHead} from "@unhead/vue";
import router from "@/router";
import {ArrowLeft, SquareFunction} from "lucide-vue-next";

useHead({
  title: "关于",
  meta: [
    {
      name: "description",
      content: "词相思是一款计算词语相似度的工具，利用夹角余弦值等算法，这里是算法介绍",
    },
  ],
})
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
        <n-icon><SquareFunction /></n-icon>
        <span>关于算法</span>
      </div>
    </template>

  </n-card>

  <AlgorithmDetail />

  <n-card class="border-b-0!">
    <template #header>
      <span>关于</span>
    </template>

    <div class="space-y-5 leading-7 px-2">
      <p>
        本项目以 MIT License 在
        <a href="https://github.com/moonryt/VectorSimilarity" target="_blank" class="hover:underline text-green">GitHub</a>
        上开源，欢迎各位同志贡献更好的代码和算法。
      </p>

      <p>
        我们设计架构、算法及逻辑后使用 OpenAI Codex 辅助开发逻辑部分，手写 UI。前端为 Vue3 Pinia Tailwind，后端 Python FastAPI Ollama 等。
      </p>

    </div>

  </n-card>

  <n-card class="border-b-0!">
    <template #header>
      <span>免责声明</span>
    </template>

    <div class="space-y-5 leading-7 px-2">
      <p>本站（我们）不为本站上的任何文本负责，他们都是由用户所输入，我们仅作用户输入的词语间的相似度计算，他们不能代表本站立场。</p>

      <p>本站的相似度等，存在由 AI 大模型（文本嵌入模型）生成的内容，并不100%真实可信，请注意甄别。</p>

      <p>本站的初衷为分享算法与人工智能、自然语言处理相关的知识，仅用于学习交流，不用于其他用处。</p>

      <p>本站的服务器不会存储您的任何信息，所有内容均保存在您浏览器本地，我们不为本站上的任何内容负责。</p>

    </div>

  </n-card>
</template>

<style scoped>

</style>
