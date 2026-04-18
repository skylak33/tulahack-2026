<script setup lang="ts">
import { computed } from 'vue'
import { useSearchStore } from '@/stores/search'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'

const search = useSearchStore()
const results = computed(() => search.current?.verdict ?? [])

const teamRoleLabel: Record<string, string> = {
  junior: 'Junior',
  middle: 'Middle',
  senior: 'Senior',
  lead: 'Lead',
}

function scoreColor(score: number) {
  if (score >= 80) return 'default'
  if (score >= 50) return 'secondary'
  return 'outline'
}
</script>

<template>
  <div class="space-y-3">
    <template v-if="search.loading">
      <Skeleton v-for="i in 3" :key="i" class="h-24 rounded-lg" />
    </template>

    <template v-else-if="results.length">
      <Card v-for="c in results" :key="c.candidate_id">
        <CardHeader class="pb-2">
          <div class="flex items-start justify-between">
            <div>
              <CardTitle class="text-base">{{ c.full_name }}</CardTitle>
              <CardDescription>{{ c.team_role ? teamRoleLabel[c.team_role] : '—' }}</CardDescription>
            </div>
            <Badge :variant="scoreColor(c.score)">{{ c.score }}%</Badge>
          </div>
        </CardHeader>
        <CardContent>
          <p class="text-sm text-muted-foreground">{{ c.compatibility }}</p>
          <div v-if="c.disc_profile" class="flex gap-3 mt-2 text-xs">
            <span v-for="(val, key) in c.disc_profile" :key="key" class="font-medium">
              {{ key }}: {{ val }}
            </span>
          </div>
        </CardContent>
      </Card>
    </template>

    <p v-else-if="search.current" class="text-sm text-muted-foreground">
      Кандидатов не найдено.
    </p>
  </div>
</template>
