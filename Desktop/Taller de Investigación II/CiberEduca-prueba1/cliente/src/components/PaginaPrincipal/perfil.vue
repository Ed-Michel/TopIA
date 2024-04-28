<template>
  <Estudiante :estudiante="datosEstudiante" />

</template>

<script>
import Estudiante from './estudianteInfo.vue'
import axios from 'axios';
import { mapGetters } from 'vuex';
import { URL_DATOS } from '@/utils/constantes';

export default {
  data() {
    return {
      datosEstudiante: {
      }
    };
  }, computed: {
    ...mapGetters('userStore', ['getEmail'])
  },
  components: {
    Estudiante
  },
  created() {
    let userEmail = this.getEmail;
    
    if(!userEmail){
     userEmail= localStorage.getItem('email')
    }
   
    console.log(userEmail);
      axios.get(URL_DATOS + 'api/infoAlumno/'+userEmail)
      .then(response => {
        const nombreAlumno = response.data[0].NOMBRE + ' ' + response.data[0].APPAT + " " + response.data[0].APMAT
        this.datosEstudiante = {
          nombre: nombreAlumno,
          institucion: response.data[0].ESCUELA,
          correo: response.data[0].CORREO,
        }
      
        
      })
      .catch(error => {
        console.error('Error al obtener al almuno', error);
      });
  }, mounted() {

  }
}

// Función para deshabilitar el botón de recarga del navegador
function deshabilitarRecarga() {
    // Sobrescribe la función de recarga del navegador
    window.onbeforeunload = function() {
        return "¿Estás seguro de que deseas recargar esta página?";
    };
}

// Llama a la función para deshabilitar la recarga al cargar la página
window.onload = function() {
    deshabilitarRecarga();
};
</script>
< style>


  </style>