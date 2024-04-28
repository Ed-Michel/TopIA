<template>
  <div>
    <h1>Actividades del Módulo {{ $route.params.moduleId }}</h1>
    <div id="modulos" v-for="actividad in actividades" :key="actividad.id">
  <!--   <router-link to="/actividad" class="enlace-actividad">{{ actividad.ACTNOMBRE }}</router-link>
     
      <router-link :to="'/module/' + $route.params.moduleId + '/' + actividad.ACTID", >{{ actividad.ACTNOMBRE }}</router-link> -->

      <router-link :to="{ name: 'ModuloXActividad', params: { moduleID: $route.params.moduleId, actID:actividad.ACTID } }">
      User profile
    </router-link>

    </div>
  </div>
</template>

<script>
import { URL_DATOS } from '@/utils/constantes';
import Login from '@/views/Login.vue';
import axios from 'axios';
export default {
  props: ['moduleId'],
  data() {
    return {
      actividades: [],
      id: null
    };
  },
  created() {
    this.id = this.$route.params.moduleId;
    this.traeActividades();
  },
  methods:{
    traeActividades: async function(){
     await axios.get(URL_DATOS + 'api/actividades/'+this.id)
      .then(response => {
        this.actividades = response.data;
        console.log(response.data)
      })
      .catch(error => {
        console.error('Error al obtener los módulos', error);
      });
    }
  }
}


</script>