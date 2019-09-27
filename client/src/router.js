import Vue from "vue";
import Router from "vue-router";

import girder from "./girder";
import Login from "@/views/Login.vue";
import Landing from "@/views/Landing.vue";

Vue.use(Router);

function beforeEnter(to, from, next) {
  if (!girder.rest.user) {
    next("/login");
  } else {
    next();
  }
}

export default new Router({
  routes: [
    {
      path: "/login",
      name: "login",
      component: Login
    },
    {
      path: "/",
      name: "Landing",
      component: Landing,
      beforeEnter
    }
  ]
});
