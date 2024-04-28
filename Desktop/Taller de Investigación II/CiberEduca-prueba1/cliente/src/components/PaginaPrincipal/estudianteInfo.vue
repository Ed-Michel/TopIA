<template>
  <div>
    <Navegador/>
    <h1>PERFIL DEL ESTUDIANTE</h1>
    <div class="container">
      <div class="estudiante-container"> <!-- Agregamos una clase de contenedor -->
        <div class="imagen-container">
          <img :src="estudiante.fotoPerfil" alt="Foto de perfil" />
        </div>
        <div class="info">
          <p>Nombre: {{ estudiante.nombre }}</p>
          <p>Institucion: {{ estudiante.institucion }}</p>
          <p>Email: {{ estudiante.correo }}</p>
          <button @click="cambiarContrasena">Cambiar Contraseña</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navegador from "../nav.vue"
export default {
  props: {
    estudiante: {
      type: Object,
      required: true,
    },
  },
  methods: {
    cambiarContrasena() {
      // Lógica para cambiar la contraseña
      console.log('Cambiando la contraseña...');
    },
  },mounted(){
    const storedMenuOptions = localStorage.getItem('menuOptions');
    if (storedMenuOptions) {
      this.$store.dispatch('login');
    }
  }, components:{
    Navegador
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  /* Esto centra verticalmente en la página */
}

.estudiante-container {
  /* Agregamos estilos para el contenedor del estudiante */
  display: flex;
  flex-direction: column;
  /* Cambiamos la dirección de flexión a columna */
  align-items: center;
  margin: 20px;
  text-align: center;
  /* Esto centra el texto dentro del div .estudiante */
}

.imagen-container {
  margin-bottom: 10px;
  /* Redujimos el espacio entre la imagen y la información */
}

img {
  border-radius: 50%;
}

button {
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  /* Agregamos espacio encima del botón */
}
</style>