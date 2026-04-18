<template>
  <div class="flex flex-col items-center justify-center py-16 text-center">
    <div class="w-12 h-12 rounded-2xl bg-ink-100 flex items-center justify-center mb-4">
      <component :is="iconComponent" class="w-6 h-6 text-ink-300" />
    </div>
    <p class="text-sm font-medium text-ink-500">{{ title }}</p>
    <p v-if="description" class="text-sm text-ink-300 mt-1 max-w-xs">{{ description }}</p>
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import * as Icons from 'lucide-vue-next'

const props = defineProps({
  icon: { type: String, default: 'Inbox' },
  title: { type: String, default: 'Ничего нет' },
  description: { type: String, default: '' },
})

const iconComponent = computed(() => Icons[props.icon])
</script>
