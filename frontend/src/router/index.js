import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/features/auth/LoginPage.vue'),
    meta: { public: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/features/auth/RegisterPage.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    component: () => import('@/shared/components/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/features/manager/DashboardPage.vue'),
      },
      {
        path: 'search/:id',
        name: 'SearchResult',
        component: () => import('@/features/manager/SearchResultPage.vue'),
        meta: { roles: ['manager'] }
      },
      {
        path: 'team',
        name: 'Team',
        component: () => import('@/features/team/TeamPage.vue'),
        meta: { roles: ['manager'] }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/features/profile/ProfilePage.vue'),
      },
      {
        path: 'profile/:id',
        name: 'UserProfile',
        component: () => import('@/features/profile/ProfilePage.vue'),
        meta: { roles: ['manager'] }
      },
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  await authStore.init()

  if (to.meta.public) {
    if (authStore.isAuthenticated) return { name: 'Dashboard' }
    return true
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'Login' }
  }

  if (to.meta.roles && !to.meta.roles.includes(authStore.user?.role)) {
    return { name: 'Dashboard' }
  }

  return true
})

export default router
