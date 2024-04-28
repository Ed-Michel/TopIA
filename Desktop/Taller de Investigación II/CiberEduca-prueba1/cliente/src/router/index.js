import Vue from 'vue';
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import login from '../views/Login.vue'
import home from '../views/PaginaPrincipal/Home.vue'
import registrate from '../views/registro.vue'
import profile from '../views/PaginaPrincipal/perfilView.vue'
import actividades from '../views/Modulos/menuActividad.vue'
import m1a1 from '../views/Modulos/m1a1.vue'
import cs from  '../components/ModuloUno/CustomStory.vue'
//import Actividad from '../views/menuActividad.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: login
  },
  {
    path: '/home',
    name: 'home',
    component: home
  },
  {
    path: '/registro',
    name: 'registrate',
    component: registrate
  },
  {
    path: '/profile',
    name: 'profile',
    component: profile
  },
  {
    path: '/module/:moduleId', component: actividades, props: true
  },
  {
    path: '/actividad/:actId', component: actividades, props: true
  },
  {
    name:"ModuloXActividad",path: '/module/:moduleID/:actID', component:{
     
      mounted() {
        
      },  render: function (createElement) {
        const moduleID = this.$route.params.moduleID
        const actividadId = this.$route.params.actID
        let componente = null;
       if(moduleID==1 && actividadId == 1){
          console.log("holaaa")
          componente = m1a1
        }
/*
        switch(moduleID){
          case "1":
              switch(actividadId){
                case"1":
                componente = m1a1
                break;
              }
              break;
        }*/
        return createElement(componente); // modUnoActUno es tu componente dinámico
      }
    }
    ,  props: true  
  }
  /*{
   path: '/modulo/:moduleId/:actividadId',
   name: 'Actividad',
   component: (route) => {
     // En función del moduleId y actividadId, decide qué componente cargar
     console.log( route.params.ACTID)
     //console.log(route.params.moduleId)
     const moduleId = route.params.moduleId;
     const actividadId = route.params.ACTID;
     
     // Aquí debes implementar la lógica para mapear moduleId y actividadId a los nombres de los componentes
     let componente = null;
     switch(moduleId) {
       case 'm1':
         switch(actividadId) {
           case 'a1':
             componente = M1A1;
             break;
           // Añade más casos según sea necesario para otras actividades del módulo 1
         }
         break;
       // Añade más casos según sea necesario para otros módulos
     }
     
     return componente;
   },
   props: true
 },*/
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
