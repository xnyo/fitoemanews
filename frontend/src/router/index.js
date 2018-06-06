import Vue from 'vue'
import Router from 'vue-router'

const Home = () => import(/* webpackChunkName: 'home' */ '@/components/Home')
const Login = () => import(/* webpackChunkName: 'login' */ '@/components/Login')
const SignUp = () => import(/* webpackChunkName: 'sign-up' */ '@/components/SignUp')

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    }, {
      path: '/login',
      name: 'Login',
      component: Login
    }, {
      path: '/signup',
      name: 'SignUp',
      component: SignUp
    }
  ]
})

export default router
