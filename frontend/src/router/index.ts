import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "@/views/HomeView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import Login from "@/views/LoginView.vue";
import UploadView from "@/views/member/UploadView.vue";
import ArchiveView from "@/views/member/ArchiveView.vue";
import PlaylistUploadView from "@/views/admin/PlaylistUploadView.vue";
import Store from "@/store";
import ProgramsView from "@/views/admin/ProgramsView.vue";
import CardedProgramsView from "@/views/admin/CardedProgramsView.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "home",
    component: Home,
    meta: { title: "Radiólogo", requiredAuth: "None" }
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: { title: "Radiólogo - Login", requiredAuth: "None" }
  },
  {
    path: "/programs/:id/upload",
    name: "programs-upload",
    component: UploadView,
    meta: { title: "Radiólogo - Upload", requiredAuth: "UserUpload" }
  },
  {
    path: "/programs/:id/archive",
    name: "programs-archive",
    component: ArchiveView,
    meta: { title: "Radiólogo - Arquivo", requiredAuth: "None" }
  },
  {
    path: "/playlist/upload",
    name: "playlist-upload",
    component: PlaylistUploadView,
    meta: { title: "Radiólogo - Upload Playlist", requiredAuth: "UserUpload" }
  },
  {
    path: "/administration/programs/",
    name: "all-programs",
    component: ProgramsView,
    meta: { title: "Radiólogo - Programas", requiredAuth: "ListAllPrograms" }
  },
  {
    path: "**",
    name: "not-found",
    component: NotFoundView,
    meta: { title: "Não encontrado", requiredAuth: "None" }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiredAuth == "None") {
    next();
  } else if (Store.getters.getUser == null && to.name != "login") {
    next("/");
  } else {
    next();
  }
});

router.afterEach(async (to, from) => {
  document.title = to.meta.title;
});

export default router;
