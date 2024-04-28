import Vue from 'vue'
import Vuex from 'vuex'
import userStore from './userStore';
// En tu archivo store.js

Vue.use(Vuex);

export default new Vuex.Store({
 modules:{
  userStore,
 },
  state: {
    isLoggedIn: false,
    menuOptions: [
      { label: "Inicio", to: "/" },
      { label: "Inicio de Sesion", to: "/login" },
      { label: "Registrate", to: "/registro" },
    ],
    menuHistory: [],
  },
  mutations: {
    login(state) {
      state.isLoggedIn = true;
      state.menuOptions = [
        { label: "Inicio", to: "/home" },
        { label: "Perfil", to: "/profile" },
      ];

      localStorage.setItem('menuOptions', JSON.stringify(this.menuOptions));
    },
    logout(state) {
      state.isLoggedIn = false;
      state.menuOptions = [
        { label: "Inicio", to: "/" },
        { label: "Inicio de Sesion", to: "/login" },
        { label: "Registrate", to: "/registrate" },
      ];
    },
    cambiarOpcionesMenu(state, nuevasOpciones) {
      state.menuHistory.push([...state.menuOptions]);
      state.menuOptions = nuevasOpciones;
    },
    restaurarMenuAnterior(state) {
      if (state.menuHistory.length > 0) {
        state.menuOptions = state.menuHistory.pop();
      }
    },
    addOption(state, newOption) {
      state.menuOptions.push(newOption);
    },
  },
  actions: {
    logout({ commit }) {
      commit('logout');
    },
    login({ commit }) {
      commit('login');
    },
    addOption({ commit }, newOption) {
      commit('addOption', newOption);
    },
  },
});