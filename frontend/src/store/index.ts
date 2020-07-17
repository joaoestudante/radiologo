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
  actions: {
    login: ({ commit, dispatch }, user) => {
      console.log(user.email);
      console.log(user.password);
    },
  },
  getters: {
    getLoading(state): boolean {
      return state.loading;
    },
  },
  modules: {},
});
