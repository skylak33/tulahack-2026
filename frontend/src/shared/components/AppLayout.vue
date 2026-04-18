<template>
  <div class="flex h-screen bg-surface-100 overflow-hidden">
    <!-- Sidebar -->
    <aside
      class="flex flex-col w-64 bg-ink shrink-0 transition-all duration-300"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-6 py-5 border-b border-ink-700">
        <div class="w-8 h-8 rounded-lg bg-accent flex items-center justify-center shrink-0">
          <span class="text-white font-display text-sm font-bold">TB</span>
        </div>
        <span class="font-display text-white text-sm font-semibold tracking-wide">Team Builder</span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <!-- Manager nav -->
        <template v-if="authStore.isManager">
          <NavItem to="/" icon="LayoutDashboard" label="Дашборд" />
          <NavItem to="/team" icon="Users" label="Команда" />
          <NavItem to="/profile" icon="UserCircle" label="Мой профиль" />
        </template>

        <!-- Employee/Candidate nav -->
        <template v-else>
          <NavItem to="/" icon="LayoutDashboard" label="Дашборд" />
          <NavItem to="/profile" icon="UserCircle" label="Мой профиль" />
        </template>
      </nav>

      <!-- User footer -->
      <div class="p-4 border-t border-ink-700">
        <div class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-ink-700 transition-colors cursor-pointer" @click="router.push('/profile')">
          <div class="w-8 h-8 rounded-lg bg-accent-800 flex items-center justify-center shrink-0">
            <span class="text-accent-200 text-sm font-semibold">{{ userInitials }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm text-white font-medium truncate">{{ authStore.user?.full_name || 'Пользователь' }}</p>
            <p class="text-xs text-ink-400 capitalize">{{ roleLabel }}</p>
          </div>
        </div>
        <button
          @click="handleLogout"
          class="w-full mt-2 flex items-center gap-2 px-3 py-2 rounded-xl text-ink-400 hover:text-rose-400 hover:bg-ink-700 transition-colors text-sm"
        >
          <LogOut class="w-4 h-4" />
          Выйти
        </button>
      </div>
    </aside>

    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="md:hidden fixed inset-0 bg-ink/50 z-10"
      @click="sidebarOpen = false"
    />

    <!-- Main content -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- Topbar -->
      <header class="h-14 flex items-center gap-4 px-6 bg-surface border-b border-ink-100 shrink-0">
        <button class="md:hidden btn-ghost btn-sm p-1.5" @click="sidebarOpen = !sidebarOpen">
          <Menu class="w-5 h-5" />
        </button>
        <div class="flex-1" />
        <div class="text-xs text-ink-300 font-mono">
          {{ new Date().toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' }) }}
        </div>
      </header>

      <!-- Page content -->
      <div class="flex-1 overflow-y-auto">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { LogOut, Menu } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import NavItem from './NavItem.vue'

const authStore = useAuthStore()
const router = useRouter()
const sidebarOpen = ref(false)

const userInitials = computed(() => {
  const name = authStore.user?.full_name || ''
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'U'
})

const roleLabel = computed(() => ({
  manager: 'Руководитель',
  employee: 'Сотрудник',
  candidate: 'Кандидат',
}[authStore.user?.role] || authStore.user?.role))

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
