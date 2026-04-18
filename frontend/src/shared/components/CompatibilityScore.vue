<template>
  <div class="flex items-center gap-2">
    <div class="relative w-10 h-10 shrink-0">
      <svg class="w-10 h-10 -rotate-90" viewBox="0 0 36 36">
        <circle cx="18" cy="18" r="14" fill="none" stroke="#EAECF0" stroke-width="3"/>
        <circle
          cx="18" cy="18" r="14" fill="none"
          :stroke="color"
          stroke-width="3"
          stroke-linecap="round"
          :stroke-dasharray="`${circumference}`"
          :stroke-dashoffset="dashOffset"
          class="transition-all duration-700"
        />
      </svg>
      <span class="absolute inset-0 flex items-center justify-center text-xs font-bold font-mono" :style="{ color }">
        {{ score }}
      </span>
    </div>
    <div v-if="showLabel">
      <p class="text-xs font-medium" :style="{ color }">{{ label }}</p>
      <p class="text-xs text-ink-300">совместимость</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: { type: Number, default: 0 },
  showLabel: { type: Boolean, default: false },
})

const circumference = 2 * Math.PI * 14  // ~87.96

const dashOffset = computed(() => circumference - (props.score / 100) * circumference)

const color = computed(() => {
  if (props.score >= 80) return '#10B981'
  if (props.score >= 60) return '#F59E0B'
  return '#F43F5E'
})

const label = computed(() => {
  if (props.score >= 80) return 'Отлично'
  if (props.score >= 60) return 'Хорошо'
  return 'Слабо'
})
</script>
