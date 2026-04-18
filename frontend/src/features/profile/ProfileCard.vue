<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Separator } from '@/components/ui/separator'

const auth = useAuthStore()
const user = computed(() => auth.user)

const roleLabel: Record<string, string> = {
  manager: 'Руководитель',
  employee: 'Сотрудник',
  candidate: 'Кандидат',
}

const teamRoleLabel: Record<string, string> = {
  junior: 'Junior',
  middle: 'Middle',
  senior: 'Senior',
  lead: 'Lead',
}

const initials = computed(() => {
  if (!user.value?.full_name) return '?'
  return user.value.full_name
    .split(' ')
    .map((w) => w[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
})
</script>

<template>
  <Card v-if="user">
    <CardHeader>
      <div class="flex items-center gap-4">
        <Avatar class="h-14 w-14">
          <AvatarFallback class="text-lg">{{ initials }}</AvatarFallback>
        </Avatar>
        <div>
          <CardTitle>{{ user.full_name }}</CardTitle>
          <p class="text-sm text-muted-foreground">{{ user.email }}</p>
        </div>
        <Badge class="ml-auto">{{ roleLabel[user.role] }}</Badge>
      </div>
    </CardHeader>
    <CardContent class="space-y-4">
      <div class="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p class="text-muted-foreground">Возраст</p>
          <p class="font-medium">{{ user.age ?? '—' }}</p>
        </div>
        <div>
          <p class="text-muted-foreground">Роль в команде</p>
          <p class="font-medium">{{ user.team_role ? teamRoleLabel[user.team_role] : '—' }}</p>
        </div>
      </div>

      <template v-if="user.disc_profile">
        <Separator />
        <div>
          <p class="text-sm font-medium mb-2">DISC-профиль</p>
          <div class="grid grid-cols-4 gap-2">
            <div v-for="(val, key) in user.disc_profile" :key="key" class="text-center">
              <div class="text-2xl font-bold">{{ val }}</div>
              <div class="text-xs text-muted-foreground">{{ key }}</div>
            </div>
          </div>
        </div>
      </template>

      <template v-if="user.motivation_profile">
        <Separator />
        <div>
          <p class="text-sm font-medium mb-2">Мотивационный профиль</p>
          <div class="space-y-1">
            <div
              v-for="(val, key) in user.motivation_profile"
              :key="String(key)"
              class="flex justify-between text-sm"
            >
              <span class="text-muted-foreground">{{ key }}</span>
              <span class="font-medium">{{ val }}</span>
            </div>
          </div>
        </div>
      </template>
    </CardContent>
  </Card>
</template>
