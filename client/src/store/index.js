import Vue from "vue";
import Vuex from "vuex";

import girder from "../girder";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    girderLocation: null,
    currentItemId: null,
    labels: []
  },
  getters: {},
  mutations: {
    setCurrentItemId(state, itemId) {
      state.currentItemId = itemId;
    },
    setGirderLocation(state, location) {
      state.girderLocation = location;
    }
  },
  actions: {
    async trySetInitialLocation({ state }) {
      if (state.girderLocation) {
        return;
      }
      var { data: collections } = await girder.rest.get("collection", {
        text: "text-annotation"
      });
      if (collections.length) {
        state.girderLocation = collections[0];
      }
    },
    async loadLabels({ state }) {
      var { data: labels } = await girder.rest.get("label");
      state.labels = labels;
    },
    async saveLabels({ state }) {
      await girder.rest.post("label", state.labels);
    }
  }
});

export default store;
