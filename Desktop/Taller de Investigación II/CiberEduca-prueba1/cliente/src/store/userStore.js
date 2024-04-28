import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const userStore = {
  namespaced: true,
  state: {
    user: {
      email: '',
      password: ''
    }
  },
  mutations: {
    setUser(state, userData) {
      state.user = userData;
      localStorage.setItem('email', userData.email);
    }
  },
  actions: {
    loginUser({ commit }, userData) {
      // Lógica de autenticación...
      console.log(userData)
      commit('setUser', userData);
    }
  },
  getters: {
    getUser: state => state.user,
    getEmail: state => state.user.email
  }
};

export default userStore;