import Vue from "vue";
import Vuex from "vuex";

import girder from "@/girder";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    selectedSampleType: null,
    meta: [],
    summary: [],
    table7: [],
    table8: [],
    table9: []
  },
  getters: {},
  mutations: {
    setSelectedSampleType(state, type) {
      state.selectedSampleType = type;
    }
  },
  actions: {
    async load({ state }) {
      var { data: records } = await girder.rest.get("record");

      Object.assign(state, {
        meta: records.map(record => ({
          ...record.meta.meta_,
          ...record.meta.meta
        })),
        summary: records
          .filter(record => record.meta.summary)
          .map(record => record.meta.summary),
        table7: records
          .filter(record => record.meta.table7)
          .map(record => record.meta.table7),
        table8: records
          .filter(record => record.meta.table8)
          .map(record => record.meta.table8),
        table9: records
          .filter(record => record.meta.table9)
          .map(record => record.meta.table9)
      });
      console.log(state);
    }
  }
});

export default store;
