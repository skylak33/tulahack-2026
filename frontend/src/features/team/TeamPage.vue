<template>
  <div class="p-8 max-w-5xl mx-auto">
    <div class="page-header flex items-start justify-between">
      <div>
        <h1 class="page-title">Моя команда</h1>
        <p class="page-subtitle">Управление составом и просмотр профилей</p>
      </div>
      <button class="btn-primary btn-md" @click="showCreateTeam = true">
        <Plus class="w-4 h-4" />
        Новая команда
      </button>
    </div>

    <Spinner v-if="teamsStore.loading && !teamsStore.teams.length" full-page />

    <EmptyState
      v-else-if="!teamsStore.teams.length"
      icon="Users"
      title="Команд пока нет"
      description="Создайте первую команду, чтобы начать работу"
    >
      <button class="btn-primary btn-md mt-4" @click="showCreateTeam = true">
        <Plus class="w-4 h-4" />
        Создать команду
      </button>
    </EmptyState>

    <div v-else class="space-y-6">
      <div
        v-for="team in teamsStore.teams"
        :key="team.id"
        class="card animate-slide-up"
      >
        <!-- Team header -->
        <div class="flex items-center justify-between mb-5">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-accent-50 border border-accent-100 flex items-center justify-center">
              <Users class="w-4 h-4 text-accent" />
            </div>
            <div>
              <h2 class="font-semibold text-ink">{{ team.name }}</h2>
              <p class="text-xs text-ink-400">{{ team.members?.length || 0 }} участников</p>
            </div>
          </div>
          <button class="btn-secondary btn-sm" @click="openAddMember(team)">
            <UserPlus class="w-4 h-4" />
            Добавить
          </button>
        </div>

        <!-- Members -->
        <div v-if="team.members?.length" class="space-y-2 animate-stagger">
          <div
            v-for="member in team.members"
            :key="member.id"
            class="flex items-center justify-between p-3 rounded-xl hover:bg-surface-100 transition-colors group"
          >
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-accent-300 to-accent-500 flex items-center justify-center text-white text-sm font-bold">
                {{ memberInitials(member) }}
              </div>
              <div>
                <p class="text-sm font-medium text-ink">{{ member.full_name }}</p>
                <div class="flex items-center gap-2 mt-0.5">
                  <span class="text-xs text-ink-400">{{ member.team_role || 'Роль не указана' }}</span>
                  <span v-if="member.age" class="text-xs text-ink-300">· {{ member.age }} лет</span>
                </div>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <RouterLink :to="`/profile/${member.id}`" class="btn-ghost btn-sm opacity-0 group-hover:opacity-100 transition-opacity">
                <Eye class="w-4 h-4" />
              </RouterLink>
              <button
                class="btn-danger btn-sm opacity-0 group-hover:opacity-100 transition-opacity"
                @click="handleRemoveMember(team.id, member.id)"
              >
                <UserMinus class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-6">
          <p class="text-sm text-ink-400">В команде пока нет участников</p>
        </div>
      </div>
    </div>

    <!-- Create team modal -->
    <Teleport to="body">
      <div v-if="showCreateTeam" class="fixed inset-0 bg-ink/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="card w-full max-w-md animate-scale-in">
          <h2 class="font-semibold text-ink mb-4">Создать команду</h2>
          <div>
            <label class="label">Название команды</label>
            <input v-model="newTeamName" type="text" class="input-base" placeholder="Например: Frontend Core" autofocus />
          </div>
          <div class="flex gap-3 mt-5">
            <button class="btn-primary btn-md" :disabled="!newTeamName.trim() || teamsStore.loading" @click="handleCreateTeam">
              <Spinner v-if="teamsStore.loading" size="sm" />
              Создать
            </button>
            <button class="btn-secondary btn-md" @click="showCreateTeam = false">Отмена</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Add member modal -->
    <Teleport to="body">
      <div v-if="showAddMember" class="fixed inset-0 bg-ink/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="card w-full max-w-md animate-scale-in">
          <h2 class="font-semibold text-ink mb-4">Добавить участника</h2>
          <div>
            <label class="label">ID пользователя</label>
            <input v-model="newMemberId" type="text" class="input-base" placeholder="Введите ID сотрудника или кандидата" />
          </div>
          <div class="flex gap-3 mt-5">
            <button class="btn-primary btn-md" :disabled="!newMemberId.trim() || teamsStore.loading" @click="handleAddMember">
              <Spinner v-if="teamsStore.loading" size="sm" />
              Добавить
            </button>
            <button class="btn-secondary btn-md" @click="showAddMember = false">Отмена</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { Plus, Users, UserPlus, UserMinus, Eye } from 'lucide-vue-next'
import { useTeamsStore } from '@/stores/teams'
import Spinner from '@/shared/components/Spinner.vue'
import EmptyState from '@/shared/components/EmptyState.vue'

const teamsStore = useTeamsStore()

const showCreateTeam = ref(false)
const showAddMember = ref(false)
const newTeamName = ref('')
const newMemberId = ref('')
const selectedTeamId = ref(null)

onMounted(() => teamsStore.fetchTeams())

function memberInitials(member) {
  return (member.full_name || '').split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'U'
}

async function handleCreateTeam() {
  const team = await teamsStore.createTeam(newTeamName.value.trim())
  if (team) { showCreateTeam.value = false; newTeamName.value = '' }
}

function openAddMember(team) {
  selectedTeamId.value = team.id
  newMemberId.value = ''
  showAddMember.value = true
}

async function handleAddMember() {
  await teamsStore.addMember(selectedTeamId.value, newMemberId.value.trim())
  showAddMember.value = false
}

async function handleRemoveMember(teamId, userId) {
  if (confirm('Удалить участника из команды?')) {
    await teamsStore.removeMember(teamId, userId)
  }
}
</script>
