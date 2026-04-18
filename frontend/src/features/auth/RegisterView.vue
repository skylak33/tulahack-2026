<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const fullName = ref('')
const role = ref<'manager' | 'employee' | 'candidate'>('employee')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await auth.register(email.value, password.value, fullName.value, role.value)
    router.push({ name: 'dashboard' })
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-background">
    <Card class="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Регистрация</CardTitle>
        <CardDescription>Создайте аккаунт</CardDescription>
      </CardHeader>
      <CardContent>
        <form class="space-y-4" @submit.prevent="handleRegister">
          <div class="space-y-1">
            <Label for="name">Имя</Label>
            <Input id="name" v-model="fullName" type="text" placeholder="Иван Иванов" required />
          </div>
          <div class="space-y-1">
            <Label for="email">Email</Label>
            <Input id="email" v-model="email" type="email" placeholder="you@example.com" required />
          </div>
          <div class="space-y-1">
            <Label for="password">Пароль</Label>
            <Input id="password" v-model="password" type="password" required />
          </div>
          <div class="space-y-1">
            <Label for="role">Роль</Label>
            <select
              id="role"
              v-model="role"
              class="w-full border border-input bg-background rounded-md px-3 py-2 text-sm"
            >
              <option value="manager">Руководитель</option>
              <option value="employee">Сотрудник</option>
              <option value="candidate">Кандидат</option>
            </select>
          </div>
          <p v-if="error" class="text-sm text-destructive">{{ error }}</p>
          <Button type="submit" class="w-full" :disabled="loading">
            {{ loading ? 'Регистрируем...' : 'Зарегистрироваться' }}
          </Button>
          <p class="text-sm text-center text-muted-foreground">
            Уже есть аккаунт?
            <RouterLink to="/login" class="text-primary underline">Войти</RouterLink>
          </p>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
