import Vue from "vue";
import Router from "vue-router";

import girder from "./girder";
import Login from "@/views/Login.vue";
import Landing from "@/views/Landing.vue";
import Data from "@/views/Data.vue";
import Workspace from "@/views/Workspace.vue";

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
    },
    {
      path: "/data",
      name: "Data",
      component: Data,
      beforeEnter
    },
    {
      path: "/workspace/:workspaceId?",
      name: "Workspace",
      component: Workspace,
      beforeEnter
    }
  ]
});
