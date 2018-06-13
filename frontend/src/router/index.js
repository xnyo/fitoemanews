import Vue from 'vue'
import Router from 'vue-router'
import Store from '@/store'

const Home = () => import(/* webpackChunkName: 'home' */ '@/components/Home')
const Login = () => import(/* webpackChunkName: 'login' */ '@/components/Login')
const SignUp = () => import(/* webpackChunkName: 'sign-up' */ '@/components/SignUp/Page')
const Activate = () => import(/* webpackChunkName: 'sign-up-activate' */ '@/components/SignUp/ActivatePage')
const NotificationSettings = () => import(/* webpackChunkName: 'notification-settings' */ '@/components/NotificationSettings/Page')
const ApiKeys = () => import(/* webpackChunkName: 'api-keys' */ '@/components/ApiKeys/Page')

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {
        protected: true,
        title: 'EmaNews',
        subtitle: 'Lista farmaci a base di erbe per uso umano'
      }
    }, {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        guestsOnly: true,
        title: 'Login',
        subtitle: 'Inserisci le tue credenziali per accedere'
      }
    }, {
      path: '/signup',
      name: 'SignUp',
      component: SignUp,
      meta: {
        guestsOnly: true,
        title: 'Registrazione',
        subtitle: 'Inserisci i tuoi dati e crea un nuovo account'
      }
    }, {
      path: '/activate/:token',
      name: 'Activate',
      component: Activate,
      meta: {
        guestsOnly: true,
        title: 'Attivazione account'
      }
    }, {
      path: '/notification_settings',
      name: 'NotificationSettings',
      component: NotificationSettings,
      meta: {
        protected: true,
        title: 'Impostazioni notifiche',
        subtitle: 'Scegli quando essere notificato da EmaNews'
      }
    }, {
      path: '/api_keys',
      name: 'ApiKeys',
      component: ApiKeys,
      meta: {
        protected: true,
        title: 'API Keys',
        subtitle: 'Usa i dati forniti da EmaNews fuori dal nostro sito'
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (Store.state.loggingIn) {
    console.log('still logging in, skipping router beforeeach')
    next()
    return
  }
  console.log('in beforeeach')
  if (to.meta.hasOwnProperty('protected') && to.meta.protected && !Store.getters.loggedIn) {
    next('/login')
  } else if (to.meta.hasOwnProperty('guestsOnly') && to.meta.guestsOnly && Store.getters.loggedIn) {
    next('/')
  } else {
    next()
  }
})

router.afterEach((to, from) => {
  Store.commit('setHeader', {
    title: to.meta.title,
    subtitle: to.meta.subtitle,
    colour: to.meta.colour
  })
  document.title = `Emanews - ${to.meta.title}`
})

export default router
