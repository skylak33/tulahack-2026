<template>
  <div
    class="flex items-start gap-4 p-4 rounded-xl border border-ink-100 hover:border-accent-200 hover:bg-accent-50/30 transition-all cursor-pointer group"
    @click="router.push(`/profile/${candidate.user_id || candidate.id}`)"
  >
    <!-- Avatar -->
    <div class="w-10 h-10 rounded-xl bg-gradient-to-br flex items-center justify-center shrink-0 text-sm font-bold text-white"
      :class="avatarGradient"
    >
      {{ initials }}
    </div>

    <!-- Info -->
    <div class="flex-1 min-w-0">
      <div class="flex items-start justify-between gap-2">
        <div>
          <p class="font-semibold text-ink text-sm group-hover:text-accent transition-colors">
            {{ candidate.full_name || 'Кандидат' }}
          </p>
          <p class="text-xs text-ink-400 mt-0.5">{{ candidate.team_role || 'Роль не указана' }}</p>
        </div>
        <CompatibilityScore :score="candidate.compatibility_score ?? candidate.score ?? 0" />
      </div>

      <!-- Tags -->
      <div class="flex flex-wrap gap-1.5 mt-2">
        <span v-if="candidate.disc_type" class="badge-accent">DISC: {{ candidate.disc_type }}</span>
        <span v-if="candidate.age" class="badge-ink">{{ candidate.age }} лет</span>
        <span v-for="tag in motivationTags" :key="tag" class="badge-jade">{{ tag }}</span>
      </div>

      <!-- AI description -->
      <p v-if="candidate.description" class="text-xs text-ink-400 mt-2 line-clamp-2">
        {{ candidate.description }}
      </p>
    </div>

    <ChevronRight class="w-4 h-4 text-ink-200 group-hover:text-accent transition-colors shrink-0 mt-1" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronRight } from 'lucide-vue-next'
import CompatibilityScore from '@/shared/components/CompatibilityScore.vue'

const props = defineProps({
  candidate: { type: Object, required: true },
})

const router = useRouter()

const initials = computed(() => {
  const name = props.candidate.full_name || ''
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'K'
})

const gradients = [
  'from-accent-400 to-accent-600',
  'from-jade-400 to-jade-600',
  'from-amber-400 to-amber-600',
  'from-rose-400 to-rose-600',
]
const avatarGradient = computed(() => {
  const idx = (props.candidate.id || 0) % gradients.length
  return gradients[idx]
})

const motivationTags = computed(() => {
  const m = props.candidate.motivation_profile
  if (!m) return []
  if (Array.isArray(m)) return m.slice(0, 2)
  if (typeof m === 'object') return Object.keys(m).slice(0, 2)
  return []
})
</script>
