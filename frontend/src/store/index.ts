import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    loading: false,
  },
  mutations: {
    stopLoading(state) {
      state.loading = false;
    },
    startLoading(state) {
      state.loading = true;
    },
  },
  actions: {},
  getters: {
    getLoading(state): boolean {
      return state.loading;
    },
  },
  modules: {},
});
