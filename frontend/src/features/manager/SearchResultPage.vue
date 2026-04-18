<template>
  <div class="p-8 max-w-4xl mx-auto">
    <button class="btn-ghost btn-sm mb-6" @click="router.back()">
      <ArrowLeft class="w-4 h-4" />
      Назад
    </button>

    <Spinner v-if="searchStore.loading" full-page />

    <SearchResultCard
      v-else-if="searchStore.currentSearch"
      :search="searchStore.currentSearch"
      expanded
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'
import { useSearchStore } from '@/stores/search'
import Spinner from '@/shared/components/Spinner.vue'
import SearchResultCard from './SearchResultCard.vue'

const route = useRoute()
const router = useRouter()
const searchStore = useSearchStore()

onMounted(() => searchStore.getSearch(route.params.id))
</script>
