import Vue from "vue";
import Vuex from "vuex";

// import girder from "@/girder";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    selectedBiomes: [],
    selectedFeatures: [],
    selectedMaterials: [],
    selectedRegion: null
  },
  getters: {},
  mutations: {
    setSelectedBiomes(state, biomes) {
      state.selectedBiomes = biomes;
    },
    setSelectedFeatures(state, features) {
      state.selectedFeatures = features;
    },
    setSelectedMaterials(state, materials) {
      state.selectedMaterials = materials;
    },
    setSelectedRegion(state, region) {
      state.selectedRegion = region;
    }
  },
  actions: {}
});

export default store;
