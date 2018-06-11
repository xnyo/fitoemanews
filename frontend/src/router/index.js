import Vue from 'vue'
import Router from 'vue-router'
import Store from '@/store'

const Home = () => import(/* webpackChunkName: 'home' */ '@/components/Home')
const Login = () => import(/* webpackChunkName: 'login' */ '@/components/Login')
const SignUp = () => import(/* webpackChunkName: 'sign-up' */ '@/components/SignUp/Page')
const Activate = () => import(/* webpackChunkName: 'sign-up-activate' */ '@/components/SignUp/ActivatePage')

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {
        protected: true
      }
    }, {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        guestsOnly: true
      }
    }, {
      path: '/signup',
      name: 'SignUp',
      component: SignUp,
      meta: {
        guestsOnly: true
      }
    }, {
      path: '/activate/:token',
      name: 'Activate',
      component: Activate,
      meta: {
        guestsOnly: true
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

export default router
