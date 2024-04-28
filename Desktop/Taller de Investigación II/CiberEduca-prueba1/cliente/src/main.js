import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Vuex from 'vuex'
import userStore from './store/userStore'

Vue.config.productionTip = false
//App.use(auth);
new Vue({
  router,
  store,
  userStore,

  render: function (h) { return h(App) }
}).$mount('#app')
