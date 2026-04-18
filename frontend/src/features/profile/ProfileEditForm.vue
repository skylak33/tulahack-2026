<template>
  <form @submit.prevent="handleSave" class="space-y-6">
    <!-- Basic info -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div>
        <label class="label">Полное имя</label>
        <input v-model="form.full_name" type="text" class="input-base" />
      </div>
      <div>
        <label class="label">Возраст</label>
        <input v-model.number="form.age" type="number" min="16" max="80" class="input-base" />
      </div>
      <div>
        <label class="label">Роль в команде</label>
        <select v-model="form.team_role" class="input-base">
          <option value="">Не выбрана</option>
          <option v-for="r in teamRoles" :key="r.value" :value="r.value">{{ r.label }}</option>
        </select>
      </div>
    </div>

    <div class="divider" />

    <!-- DISC Profile -->
    <div>
      <h3 class="font-semibold text-ink text-sm mb-4 flex items-center gap-2">
        <BarChart2 class="w-4 h-4 text-accent" />
        DISC профиль
        <span class="text-xs text-ink-300 font-normal">(0–100 для каждой шкалы)</span>
      </h3>
      <div class="grid grid-cols-2 gap-4">
        <div v-for="key in ['D','I','S','C']" :key="key">
          <label class="label flex items-center gap-2">
            <span class="w-5 h-5 rounded-md flex items-center justify-center text-xs font-bold" :class="discColors[key].bg">{{ key }}</span>
            {{ discColors[key].label }}
          </label>
          <input
            v-model.number="form.disc_profile[key]"
            type="number" min="0" max="100"
            class="input-base font-mono"
            placeholder="0–100"
          />
        </div>
      </div>
    </div>

    <div class="divider" />

    <!-- Motivation Profile (key-value pairs) -->
    <div>
      <h3 class="font-semibold text-ink text-sm mb-4 flex items-center gap-2">
        <Zap class="w-4 h-4 text-accent" />
        Мотивационный профиль
      </h3>
      <div class="space-y-2">
        <div
          v-for="(item, idx) in motivationItems"
          :key="idx"
          class="flex items-center gap-2"
        >
          <input v-model="item.key" type="text" class="input-base flex-1" placeholder="Фактор" />
          <input v-model="item.value" type="text" class="input-base w-24" placeholder="Значение" />
          <button type="button" class="btn-ghost btn-sm p-2 text-rose-400" @click="removeMotivation(idx)">
            <Trash2 class="w-4 h-4" />
          </button>
        </div>
        <button type="button" class="btn-secondary btn-sm" @click="addMotivation">
          <Plus class="w-4 h-4" />
          Добавить фактор
        </button>
      </div>
    </div>

    <div v-if="error" class="p-3 rounded-xl bg-rose-50 border border-rose-100">
      <p class="text-sm text-rose-600">{{ error }}</p>
    </div>

    <div class="flex gap-3">
      <button type="submit" class="btn-primary btn-md" :disabled="saving">
        <Spinner v-if="saving" size="sm" />
        {{ saving ? 'Сохраняем...' : 'Сохранить' }}
      </button>
      <button type="button" class="btn-secondary btn-md" @click="$emit('cancel')">Отмена</button>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { BarChart2, Zap, Trash2, Plus } from 'lucide-vue-next'
import { usersApi } from '@/shared/api/users'
import Spinner from '@/shared/components/Spinner.vue'

const props = defineProps({ user: { type: Object, required: true } })
const emit = defineEmits(['saved', 'cancel'])

const saving = ref(false)
const error = ref(null)

const form = reactive({
  full_name: props.user.full_name || '',
  age: props.user.age || null,
  team_role: props.user.team_role || '',
  disc_profile: { D: 0, I: 0, S: 0, C: 0, ...props.user.disc_profile },
})

const motivationItems = ref(
  Object.entries(props.user.motivation_profile || {}).map(([key, value]) => ({ key, value }))
)

const teamRoles = [
  { value: 'junior', label: 'Junior' },
  { value: 'middle', label: 'Middle' },
  { value: 'senior', label: 'Senior' },
  { value: 'lead', label: 'Lead' },
  { value: 'manager', label: 'Manager' },
  { value: 'director', label: 'Director' },
]

const discColors = {
  D: { label: 'Доминирование', bg: 'bg-rose-50 text-rose-500' },
  I: { label: 'Влияние',       bg: 'bg-amber-50 text-amber-500' },
  S: { label: 'Стабильность',  bg: 'bg-jade-50 text-jade-500' },
  C: { label: 'Соответствие',  bg: 'bg-accent-50 text-accent' },
}

function addMotivation() { motivationItems.value.push({ key: '', value: '' }) }
function removeMotivation(idx) { motivationItems.value.splice(idx, 1) }

async function handleSave() {
  saving.value = true
  error.value = null
  try {
    const motivation_profile = {}
    motivationItems.value.forEach(({ key, value }) => {
      if (key.trim()) motivation_profile[key.trim()] = value
    })
    const payload = { ...form, motivation_profile }
    const { data } = await usersApi.updateMe(payload)
    emit('saved', data)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка сохранения'
  } finally {
    saving.value = false
  }
}
</script>
