import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'

import Home from '../views/Home.vue'

import Product from '../views/Product.vue'
import Users from '../views/Users.vue'
import Search from '../views/Search.vue'
import Cart from '../views/Cart.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import MyAccount from '../views/MyAccount.vue'
import Checkout from '../views/CheckOut.vue'
import Success from '../views/Success.vue'
import UserStore from '../views/UserStore.vue'
import AddProduct from '../views/AddProduct.vue'
import MyStore from '../views/MyStore.vue'
import ChargeBalance from '../views/ChargeBalance.vue' 
import EditProduct from '../views/EditProduct.vue'
import Admin from '../views/Admin.vue'




const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta: {
        requireLogin: true
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: Search,
    meta: {
        requireLogin: true
    }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/cart/success',
    name: 'Success',
    component: Success,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/cart/checkout',
    name: 'Checkout',
    component: Checkout,
    meta: {
        requireLogin: true
    }
  },
  {
    path: '/:username/products/:id',
    name: 'Product',
    component: Product,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/users/:username',
    name: 'UserStore',
    component: UserStore,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/users',
    name: 'Users',
    component: Users,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/my-store/add-product',
    name: 'AddProduct',
    component: AddProduct,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/my-store/edit-product/:id',
    name: 'EditProduct',
    component: EditProduct,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/my-store',
    name: 'MyStore',
    component: MyStore,
    meta: {
      requireLogin: true
    }
  },
  {
    path:'/my-account/charge-balance',
    name:'ChargeBalance',
    component:ChargeBalance,
    meta: {
      requireLogin: true
    }
  },
  {
    path:'/admin-panel',
    name:'AdminPanel',
    component:Admin,
    meta: {
      requireLogin: true
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'LogIn', query: { to: to.path } });
  } else {
    next()
  }
})

export default router
