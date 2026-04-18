<template>
  <div>
    <!-- Header -->
    <div class="page-header flex items-start justify-between">
      <div>
        <h1 class="page-title">Подбор сотрудника</h1>
        <p class="page-subtitle">Опишите нужного кандидата — AI найдёт лучших</p>
      </div>
      <div class="flex items-center gap-2 text-sm text-ink-400 bg-surface rounded-xl px-3 py-2 border border-ink-100">
        <Sparkles class="w-4 h-4 text-accent" />
        Powered by Gemini
      </div>
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- Search form — main column -->
      <div class="xl:col-span-2 space-y-5">
        <!-- Search card -->
        <div class="card">
          <div class="flex items-center gap-2 mb-4">
            <Search class="w-4 h-4 text-accent" />
            <h2 class="font-semibold text-ink">Новый поиск</h2>
          </div>

          <div class="space-y-4">
            <div>
              <label class="label">Описание вакансии / требований</label>
              <textarea
                v-model="queryText"
                class="input-base resize-none"
                rows="5"
                placeholder="Например: Нужен senior frontend разработчик с опытом в Vue.js, умеющий работать в быстрой команде стартапа. Важна инициативность и самостоятельность. Желательно наличие лидерских качеств..."
              />
              <p class="text-xs text-ink-300 mt-1.5">{{ queryText.length }} символов · минимум 20</p>
            </div>

            <button
              class="btn-primary btn-md w-full"
              :disabled="queryText.length < 20 || searchStore.loading"
              @click="handleSearch"
            >
              <Spinner v-if="searchStore.loading" size="sm" />
              <Sparkles v-else class="w-4 h-4" />
              {{ searchStore.loading ? 'Анализируем...' : 'Найти кандидатов' }}
            </button>
          </div>
        </div>

        <!-- Current search result -->
        <SearchResultCard
          v-if="searchStore.currentSearch"
          :search="searchStore.currentSearch"
          expanded
        />
      </div>

      <!-- History sidebar -->
      <div class="space-y-4">
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2">
              <Clock class="w-4 h-4 text-ink-400" />
              <h2 class="font-semibold text-ink text-sm">История запросов</h2>
            </div>
            <span class="badge-ink">{{ searchStore.history.length }}</span>
          </div>

          <Spinner v-if="searchStore.loading && !searchStore.history.length" />

          <EmptyState
            v-else-if="!searchStore.history.length"
            icon="Search"
            title="Нет запросов"
            description="Результаты поиска появятся здесь"
          />

          <div v-else class="space-y-2">
            <button
              v-for="item in searchStore.history"
              :key="item.id"
              class="w-full text-left p-3 rounded-xl border border-transparent hover:border-ink-200 hover:bg-surface-50 transition-all group"
              @click="loadSearch(item.id)"
            >
              <p class="text-sm text-ink font-medium line-clamp-2 group-hover:text-accent transition-colors">
                {{ item.query_text }}
              </p>
              <div class="flex items-center gap-2 mt-1.5">
                <span class="text-xs text-ink-300">{{ formatDate(item.created_at) }}</span>
                <span v-if="item.verdict?.length" class="badge-jade text-xs">
                  {{ item.verdict.length }} кандидатов
                </span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Clock, Sparkles } from 'lucide-vue-next'
import { useSearchStore } from '@/stores/search'
import Spinner from '@/shared/components/Spinner.vue'
import EmptyState from '@/shared/components/EmptyState.vue'
import SearchResultCard from './SearchResultCard.vue'

const searchStore = useSearchStore()
const queryText = ref('')

onMounted(() => searchStore.fetchHistory())

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
}

async function handleSearch() {
  await searchStore.createSearch(queryText.value)
}

async function loadSearch(id) {
  await searchStore.getSearch(id)
}
</script>
