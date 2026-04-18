<template>
  <div class="space-y-3">
    <div v-for="(item, key) in items" :key="key" class="space-y-1.5">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span
            class="w-5 h-5 rounded-md flex items-center justify-center text-xs font-bold font-display"
            :class="item.bg"
          >{{ key }}</span>
          <span class="text-sm text-ink-500">{{ item.label }}</span>
        </div>
        <span class="text-sm font-semibold font-mono" :class="item.color">{{ disc[key] ?? 0 }}</span>
      </div>
      <div class="h-2 bg-ink-100 rounded-full overflow-hidden">
        <div
          class="h-full rounded-full transition-all duration-700 ease-out"
          :class="item.bar"
          :style="{ width: `${disc[key] ?? 0}%` }"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  disc: { type: Object, default: () => ({ D: 0, I: 0, S: 0, C: 0 }) }
})

const items = {
  D: { label: 'Доминирование', color: 'text-rose-500', bg: 'bg-rose-50 text-rose-500', bar: 'bg-rose-400' },
  I: { label: 'Влияние',       color: 'text-amber-500', bg: 'bg-amber-50 text-amber-500', bar: 'bg-amber-400' },
  S: { label: 'Стабильность',  color: 'text-jade-500',  bg: 'bg-jade-50 text-jade-500',  bar: 'bg-jade-400' },
  C: { label: 'Соответствие',  color: 'text-accent',    bg: 'bg-accent-50 text-accent',  bar: 'bg-accent-400' },
}
</script>
