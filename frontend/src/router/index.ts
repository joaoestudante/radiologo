import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "@/views/HomeView.vue";
import NotFoundView from "@/views/NotFoundView.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "**",
    name: "not-found",
    component: NotFoundView,
    meta: { title: "Page Not Found", requiredAuth: "None" },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
