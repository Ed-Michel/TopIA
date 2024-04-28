<template>
  <div class="seccion-con-imagen">
    <img :src="imagenSrc" alt="Imagen de la sección" class="imagen-seccion">
    <p class="texto-seccion">{{ texto }}</p>
    <p class="progreso">{{ progreso }}</p>
    <router-link :to="enlaceDestino" class="enlace-actividad">Ir a la Actividad</router-link>
  </div>
</template>

<script>
export default {
  props: {
    imagenSrc: {
      type: String,
      required: true,
    },
    enlaceDestino: {
      type: String,
      required: true,
    },
    texto:{
        type: String,
        required: true,
    },
    progreso:{
      type: Number,
      required:true,
    },
    computed: {
    enlaceDestino() {
      return `/module/${this.moduloId}`;
    }
  }
  },
};

</script>

<style scoped>
/* Estilos específicos del componente */
.seccion-con-imagen {
  text-align: center;
  display: flex;
  flex-direction: column; /* Alinea los elementos en columna */
  align-items: center;
  border: #007bff 1px solid; 
  width: 300px;
  height: 182px;
}

.enlace-actividad {
  text-decoration: none;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border-radius: 5px;
}
</style>