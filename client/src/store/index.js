import Vue from "vue";
import Vuex from "vuex";

import girder from "@/girder";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    meta: [],
    summary: [],
    table7: [],
    table8: [],
    table9: []
  },
  getters: {},
  mutations: {},
  actions: {
    async load({ state }) {
      var { data: records } = await girder.rest.get("record");
      state.meta = records.meta;
      Object.assign(state, records);
      console.log(state);
    }
  }
});

export default store;
