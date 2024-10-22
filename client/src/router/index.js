import { createRouter, createWebHistory } from 'vue-router'
import MembersView from '../views/MembersView.vue'
import GroupsView from '../views/GroupsView.vue'
import AlbumsView from '../views/AlbumsView.vue'
import SongsView from '../views/SongsView.vue'
import GenresView from '../views/GenresView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{
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
    },
  ]
})

export default router
