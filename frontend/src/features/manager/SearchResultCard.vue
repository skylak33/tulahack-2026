<template>
  <div class="card animate-slide-up">
    <div class="flex items-center justify-between mb-5">
      <div>
        <h2 class="font-semibold text-ink flex items-center gap-2">
          <Users class="w-4 h-4 text-accent" />
          Результаты подбора
        </h2>
        <p class="text-xs text-ink-400 mt-0.5 line-clamp-1">{{ search.query_text }}</p>
      </div>
      <span class="badge-accent">{{ candidates.length }} кандидатов</span>
    </div>

    <div v-if="!candidates.length" class="py-8 text-center">
      <p class="text-sm text-ink-400">Нет подходящих кандидатов по данному запросу</p>
    </div>

    <div v-else class="space-y-3 animate-stagger">
      <CandidateCard
        v-for="candidate in candidates"
        :key="candidate.id || candidate.user_id"
        :candidate="candidate"
      />
    </div>

    <div v-if="search.verdict?.summary" class="mt-4 p-3 rounded-xl bg-surface-50 border border-ink-100">
      <p class="text-xs font-semibold text-ink-400 mb-1 uppercase tracking-wide">Вывод Gemini</p>
      <p class="text-sm text-ink-500">{{ search.verdict.summary }}</p>
    </div>

    <p class="text-xs text-ink-300 mt-4">
      Запрос создан {{ formatDate(search.created_at) }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Users } from 'lucide-vue-next'
import CandidateCard from './CandidateCard.vue'

const props = defineProps({
  search: { type: Object, required: true },
  expanded: { type: Boolean, default: false },
})

const candidates = computed(() => props.search.verdict?.candidates || [])

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
}
</script>
