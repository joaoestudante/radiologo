import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "@/views/HomeView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import Login from "@/views/LoginView.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { title: "Radiólogo", requiredAuth: "None" }
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { title: "Radiólogo - Login", requiredAuth: "None" }
  },
  {
    path: "**",
    name: "not-found",
    component: NotFoundView,
    meta: { title: "Page Not Found", requiredAuth: "None" }
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
  } else {
    next("/");
  }
});

router.afterEach(async (to, from) => {
  document.title = to.meta.title;
});

export default router;
