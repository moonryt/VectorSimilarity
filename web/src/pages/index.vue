<script setup lang="ts">

import router from "@/router";
import {BookOpenText, Scale, History, SquareFunction} from "lucide-vue-next";
import { useHead } from "@unhead/vue";

useHead({
  title: "首页",
  meta: [
    {
      name: "description",
      content: "词相思是一款计算词语相似度的工具，利用夹角余弦值等算法，得到两个词语的相似成都",
    },
  ],
})
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

    该小工具可以计算两个文段和词语之间的相似度。您可以输入两个词汇或两段文字以计算，即使不是同一个领域也可以，比如「学校」和「九转大肠」。
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

        <n-list-item class="py-5!" @click="router.push('/about')">
          <template #prefix>
            <n-icon size="25"><SquareFunction /></n-icon>
          </template>
          <n-thing title="算法原理" description="关于页，有这个程序的算法原理及相关声明">
          </n-thing>
        </n-list-item>
      </n-list>
    </div>
  </n-card>
</template>

<style scoped>

</style>
