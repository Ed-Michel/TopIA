// store.js
import Vue from 'vue';
import Vuex from 'vuex';
import authService from './authService';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('token') || null,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
  },
  actions: {
    async refreshToken({ commit }) {
      const token = await authService.refreshToken();
      commit('setToken', token);
    },
  },
});