import Vue from "vue";
import Vuex from "vuex";
import BackendServices from "@/services/BackendServices";
import AuthDto from "@/models/user/AuthDto";
import User from "@/models/user/User";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

interface State {
  loading: boolean;
  accessToken: string;
  user: User | null;
}

const state: State = {
  loading: false,
  accessToken: "",
  user: null
};

export default new Vuex.Store({
  state: state,
  mutations: {
    stopLoading(state) {
      state.loading = false;
    },
    startLoading(state) {
      state.loading = true;
    },
    login(state, authResponse: AuthDto) {
      state.accessToken = authResponse.access;
      state.user = authResponse.user;
    },
    logout(state) {
      state.user = null;
      state.accessToken = "";
    }
  },
  actions: {
    login: ({ commit, dispatch }, userDetails) => {
      return new Promise((resolve, reject) => {
        BackendServices.login(userDetails.email, userDetails.password)
          .then(authResponse => {
            commit("login", authResponse);
            resolve();
          })
          .catch(error => {
            reject(error);
          });
      });
    }
  },
  getters: {
    getLoading(state): boolean {
      return state.loading;
    },
    getToken(state): string {
      return state.accessToken;
    },
    getUser(state): User | null {
      return state.user;
    }
  },
  modules: {},
  plugins: [createPersistedState()]
});
