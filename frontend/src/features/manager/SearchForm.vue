<script setup lang="ts">
import { ref } from 'vue'
import { useSearchStore } from '@/stores/search'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'

const search = useSearchStore()
const query = ref('')
const error = ref('')

async function handleSubmit() {
  if (!query.value.trim()) return
  error.value = ''
  try {
    await search.createSearch(query.value)
    query.value = ''
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Ошибка поиска'
  }
}
</script>

<template>
  <form class="space-y-3" @submit.prevent="handleSubmit">
    <Label for="query">Опишите нужного сотрудника</Label>
    <Textarea
      id="query"
      v-model="query"
      placeholder="Например: нужен senior backend-разработчик с лидерскими качествами, склонный к детальной работе..."
      rows="4"
    />
    <p v-if="error" class="text-sm text-destructive">{{ error }}</p>
    <Button type="submit" :disabled="search.loading || !query.trim()">
      {{ search.loading ? 'Анализируем...' : 'Найти кандидатов' }}
    </Button>
  </form>
</template>
