import { createRouter, createWebHistory } from 'vue-router'
import { hideAlert } from '@/logic/alertFunctions'
import { token } from '@/logic/variables'

const macroLogin = 'macroLogin'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'macroHome',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true, authRedirect: macroLogin },
    },
    {
      path: '/login',
      name: macroLogin,
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'macroRegister',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/calender',
      name: 'macroCalender',
      component: () => import('../views/CalenderView.vue'),
      meta: { requiresAuth: true, authRedirect: macroLogin }
    },
    {
      path: '/meals',
      name: 'macroMeals',
      component: () => import('../views/MealsView.vue'),
      meta: { requiresAuth: true, authRedirect: macroLogin }
    },
    {
      path: '/ingredients',
      name: 'macroIngredients',
      component: () => import('../views/IngredientsView.vue'),
      meta: { requiresAuth: true, authRedirect: macroLogin }
    },
    {
      path: '/profile',
      name: 'macroProfile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true, authRedirect: macroLogin }
    }
  ]
})

function isAuthenticated() {
  return token.value
}

router.beforeEach((to, _, next) => {
  if (to.name != macroLogin && to.name != 'marcoHome' && to.name != 'macroProfile') {
    hideAlert()
  }

  // if (to.name != 'home') {
  //   window.scrollTo({
  //     left: 0,
  //     top: 0,
  //     behavior: 'instant'
  //   })
  // }

  if (to.meta.requiresAuth && !isAuthenticated()) {
    //console.log('User is not authed, redirecting to:', to.meta.authRedirect)
    next({ name: to.meta.authRedirect as string })
  } else {
    //console.log('Routing to website: ', to.name, 'from: ', from.name)
    next()
  }
})


export default router
