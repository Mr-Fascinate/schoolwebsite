import { createRouter, createWebHashHistory } from 'vue-router'
import Home from './views/Home.js'
import PlaceholderView from './views/PlaceholderView.js'

const routes = [
  { path: '/', component: Home },
  { path: '/about-us', component: PlaceholderView, props: { title: 'About Us' } },
  { path: '/admissions', component: PlaceholderView, props: { title: 'Admissions' } },
  { path: '/life-at-doon', component: PlaceholderView, props: { title: 'Life At Doon' } },
  { path: '/events', component: PlaceholderView, props: { title: 'Events at Doon' } },
  { path: '/centres-of-excellence', component: PlaceholderView, props: { title: 'Centres of Excellence' } },
  { path: '/updates', component: PlaceholderView, props: { title: 'Latest Updates' } },
  { path: '/alumni', component: PlaceholderView, props: { title: 'Alumni Relations' } },
  { path: '/jobs', component: PlaceholderView, props: { title: 'Jobs at Doon' } },
  { path: '/contact-us', component: PlaceholderView, props: { title: 'Contact Us' } }
]

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})
