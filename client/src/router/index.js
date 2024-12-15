import { createRouter, createWebHistory } from 'vue-router'

import MainView from '@/views/MainView.vue'
import MembersView from '../views/MembersView.vue'
import GroupsView from '../views/GroupsView.vue'
import AlbumsView from '../views/AlbumsView.vue'
import SongsView from '../views/SongsView.vue'
import GenresView from '../views/GenresView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{
        path: "/",
        name: "MainView",
        component: MainView
    },{
        path: "/groups",
        name: "GroupsView",
        component: GroupsView
    },{
        path: "/members",
        name: "MembersView",
        component: MembersView
    },{
        path: "/albums",
        name: "AlbumsView",
        component: AlbumsView
    },{
        path: "/songs",
        name: "SongsView",
        component: SongsView
    },{
        path: "/genres",
        name: "GenresView",
        component: GenresView
    },{
        path: "/login",
        name: "LoginView",
        component: LoginView
    },{
        path: "/register",
        name: "RegisterView",
        component: RegisterView
    }
  ]
})

export default router
