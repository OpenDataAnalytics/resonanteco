import Vue from "vue";
import Router from "vue-router";

import girder from "./girder";
import Login from "@/views/Login.vue";
import Home from "@/views/Home.vue";
import ItemView from "@/views/ItemView.vue";

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
      name: "Home",
      component: Home,
      beforeEnter
    },
    {
      path: "/item/:id?",
      name: "ItemView",
      component: ItemView,
      beforeEnter
    }
  ]
});
