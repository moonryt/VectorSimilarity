<script setup lang="ts">

import { RouterView } from 'vue-router'
import {darkTheme, useOsTheme, zhCN} from "naive-ui";
import { computed } from 'vue'
import { useHead } from '@unhead/vue'
import AppFooter from "@/components/AppFooter.vue";
import AppLayouts from "@/components/AppLayouts.vue";

import katex from 'katex'
import 'katex/dist/katex.css'
import router from "@/router";

const osThemeRef = useOsTheme()
const theme = computed(() => (osThemeRef.value === 'dark' ? darkTheme : null))

useHead({
  titleTemplate: (title) => title ? `${title} - 词相思 · 文字相似度计算小助手` : '词相思 文字相似度计算小助手',
  meta: [
    {
      name: 'subtitle',
      content: '词相思 · 文字相似度计算小助手',
    },
  ],
})
</script>

<template>
  <n-config-provider :theme="theme" :locale="zhCN" :katex="katex">

    <n-global-style />

    <n-dialog-provider>
      <n-loading-bar-provider>
        <n-message-provider>

          <AppLayouts />

          <div class="flex flex-row justify-center items-start min-h-screen lg:px-8 xl:px-12">
            <div class="w-full lg:w-175 max-w-300 min-h-screen">
              <n-card
                class="w-full justify-between sticky top-0 z-99 border-b-0!"
              >
                <template #header>
                  <div class="flex items-center gap-1.5 h-7 w-full cursor-pointer" @click="router.replace('/')">
                    <img src="@/assets/img/logo.png" alt="Logo" class="w-10! h-10!" />
                    <span class="text-xl font-semibold">词相思</span>
                  </div>
                </template>
              </n-card>

              <main>
                <router-view v-slot="{ Component }">
                  <keep-alive>
                    <component :is="Component" />
                  </keep-alive>
                </router-view>
              </main>

              <footer>
                <AppFooter />
              </footer>

            </div>
          </div>

        </n-message-provider>
      </n-loading-bar-provider>
    </n-dialog-provider>
  </n-config-provider>
</template>

<style scoped></style>
