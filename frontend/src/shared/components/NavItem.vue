<template>
  <RouterLink
    :to="to"
    class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all duration-150 group"
    :class="isActive
      ? 'bg-accent text-white shadow-sm'
      : 'text-ink-300 hover:text-white hover:bg-ink-700'"
  >
    <component :is="iconComponent" class="w-4 h-4 shrink-0" />
    <span class="font-medium">{{ label }}</span>
  </RouterLink>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import * as Icons from 'lucide-vue-next'

const props = defineProps({
  to: { type: String, required: true },
  icon: { type: String, required: true },
  label: { type: String, required: true },
})

const route = useRoute()
const isActive = computed(() => {
  if (props.to === '/') return route.path === '/'
  return route.path.startsWith(props.to)
})
const iconComponent = computed(() => Icons[props.icon])
</script>
