<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import ProfileCard from '@/features/profile/ProfileCard.vue'
import SearchForm from '@/features/manager/SearchForm.vue'
import SearchResults from '@/features/manager/SearchResults.vue'
import SearchHistory from '@/features/manager/SearchHistory.vue'

const auth = useAuthStore()
const router = useRouter()
const isManager = computed(() => auth.role === 'manager')

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="min-h-screen bg-background">
    <header class="border-b px-6 py-3 flex items-center justify-between">
      <h1 class="text-lg font-semibold">Team Builder</h1>
      <div class="flex items-center gap-3">
        <span class="text-sm text-muted-foreground">{{ auth.user?.full_name }}</span>
        <Button variant="outline" size="sm" @click="logout">Выйти</Button>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-6 py-8 space-y-8">
      <ProfileCard />

      <template v-if="isManager">
        <Separator />

        <Tabs default-value="search">
          <TabsList>
            <TabsTrigger value="search">Поиск кандидатов</TabsTrigger>
            <TabsTrigger value="history">История запросов</TabsTrigger>
          </TabsList>

          <TabsContent value="search" class="mt-4 space-y-6">
            <SearchForm />
            <SearchResults />
          </TabsContent>

          <TabsContent value="history" class="mt-4">
            <SearchHistory />
          </TabsContent>
        </Tabs>
      </template>
    </main>
  </div>
</template>
