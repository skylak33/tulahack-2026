<template>
  <div class="flex items-center justify-center" :class="fullPage ? 'h-64' : ''">
    <div
      class="rounded-full border-2 border-ink-200 border-t-accent animate-spin"
      :class="sizes[size]"
    />
  </div>
</template>

<script setup>
defineProps({
  size: { type: String, default: 'md' },
  fullPage: { type: Boolean, default: false },
})

const sizes = {
  sm: 'w-4 h-4',
  md: 'w-6 h-6',
  lg: 'w-10 h-10',
}
</script>
