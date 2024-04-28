<template>
  <div id="homecontenedor">
    <Navegador/>
    <h1>Tus modulos</h1>
    <div id="contenedorModulos">
      <div id="modulos" v-for="modulo in modulos" :key="modulo.id">
        <SeccionConImagen :enlaceDestino="`/module/${modulo.ID}`" :texto="modulo.MODNOMBRE" :progreso="5" :imagenSrc="'logo.png'" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import SeccionConImagen from '../modulo.vue'
import Quiz from '../../components/Quiz.vue'
import customStory from '../../components/plantilla-historia.vue'
import { URL_DATOS } from '@/utils/constantes';
import Navegador  from "../nav.vue"
export default {
  data() {
    return {
      modulos: [],
    };
  },
  created() {

  }, mounted() {
    const storedMenuOptions = localStorage.getItem('menuOptions');
    if (storedMenuOptions) {
      this.$store.dispatch('login');
    }
    axios.get(URL_DATOS + 'api/modulos')
      .then(response => {
        this.modulos = response.data;
        console.log(response.data)
      })
      .catch(error => {
        console.error('Error al obtener los módulos', error);
      });
  },
  components: {
    SeccionConImagen,
    Quiz,
    customStory,
    Navegador
  },
  methods: {
    regresar() {
      this.$store.dispatch('logout')
    },

    previousHandler() {
      console.log('Botón Anterior presionado');
    },
    nextHandler() {
      console.log('Botón Siguiente presionado');
    },
    getCustomClasses(scene) {
      const classes = ['custom-container'];
      if (scene.isFirstScene) {
        classes.push('first-scene');
      }

      return classes;
    },
  },
}

</script>
<style scoped>
/* Puedes enlazar el archivo CSS externo así: */
@import url('../../assets/home.css');



.custom-container {
  padding: 20px;
  border: 1px solid #ccc;
}

/* Estilos específicos para la primera escena */
.first-scene {
  background-color: #ffd700;
  /* Por ejemplo, color amarillo */
}
</style>