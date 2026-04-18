<script setup lang="ts">
import { onMounted } from 'vue'
import { useSearchStore } from '@/stores/search'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'

const search = useSearchStore()

onMounted(() => search.fetchHistory())

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <div class="space-y-2">
    <template v-if="search.loading && !search.history.length">
      <Skeleton v-for="i in 3" :key="i" class="h-12 rounded-md" />
    </template>

    <p v-else-if="!search.history.length" class="text-sm text-muted-foreground">
      Истории запросов нет.
    </p>

    <div
      v-for="item in search.history"
      :key="item.id"
      class="flex items-center justify-between rounded-md border px-3 py-2 text-sm"
    >
      <div class="flex-1 min-w-0">
        <p class="truncate font-medium">{{ item.query_text }}</p>
        <p class="text-xs text-muted-foreground">{{ formatDate(item.created_at) }}</p>
      </div>
      <Button variant="ghost" size="sm" @click="search.fetchById(item.id)">Открыть</Button>
    </div>
  </div>
</template>
