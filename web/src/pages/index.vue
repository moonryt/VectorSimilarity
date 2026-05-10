<script setup lang="ts">

import router from "@/router";
import {BookOpenText, Scale, History} from "lucide-vue-next";
</script>

<template>
  <n-card
    size="small"
    class="px-4 border-b-0!"
  >
    <template #header>
      <div class="flex items-center gap-3 h-7 w-full">
        <n-icon><BookOpenText /></n-icon>
        <span>介绍</span>
      </div>
    </template>

    您可以输入两个词汇或两段文字，计算它们的相似度，不要求这两个词在同一个领域，比如「学校」和「九转大肠」。
  </n-card>

  <n-card class="border-b-0!">
    <div>
      <n-list hoverable clickable>
        <n-list-item class="py-5!" @click="router.push('/compare')">
          <template #prefix>
            <n-icon size="25"><Scale /></n-icon>
          </template>
          <n-thing title="开始使用" description="开始以输入两个词进行相似度比较">
          </n-thing>
        </n-list-item>

        <n-list-item class="py-5!" @click="router.push('/history')">
          <template #prefix>
            <n-icon size="25"><History /></n-icon>
          </template>
          <n-thing title="历史记录" description="查询自己查询过的相似度计算">
          </n-thing>
        </n-list-item>
      </n-list>
    </div>
  </n-card>
</template>

<style scoped>

</style>
