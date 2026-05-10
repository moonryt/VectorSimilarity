<script setup lang="ts">
import dayjs from "dayjs"
import { ArrowLeft, History, Trash2 } from "lucide-vue-next"
import router from "@/router"
import { useVectorHistoryStore } from "@/stores/vectorHistory"

const historyStore = useVectorHistoryStore()
</script>

<template>
  <n-card class="border-b-0!">
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
          @click="historyStore.clearRecords()"
        >
          <template #icon>
            <n-icon><Trash2 /></n-icon>
          </template>
        </n-button>
      </div>
    </template>

    <n-empty v-if="historyStore.records.length === 0" description="暂无对比记录" />

    <n-list v-else hoverable>
      <n-list-item v-for="record in historyStore.latestRecords" :key="record.id" class="py-4!">
        <n-thing>
          <template #header>
            <div class="flex flex-wrap items-center gap-2">
              <n-tag size="small" type="success">{{ record.response.adjustedPercent }}</n-tag>
              <span class="text-sm text-gray-500">
                {{ dayjs(record.completedAt).format("YYYY-MM-DD HH:mm:ss") }}
              </span>
            </div>
          </template>

          <template #description>
            <div class="mt-2 grid gap-2 text-sm md:grid-cols-2">
              <n-ellipsis>{{ record.request.text1 }}</n-ellipsis>
              <n-ellipsis>{{ record.request.text2 }}</n-ellipsis>
            </div>
          </template>

          <div class="mt-3 flex flex-wrap gap-2 text-xs text-gray-500">
            <span>语义相似度：{{ record.response.percent }}</span>
            <span>模型：{{ record.response.model }}</span>
            <span>ID：{{ record.id }}</span>
          </div>

          <template #action>
            <n-button quaternary circle size="small" @click="historyStore.removeRecord(record.id)">
              <template #icon>
                <n-icon><Trash2 /></n-icon>
              </template>
            </n-button>
          </template>
        </n-thing>
      </n-list-item>
    </n-list>
  </n-card>
</template>
