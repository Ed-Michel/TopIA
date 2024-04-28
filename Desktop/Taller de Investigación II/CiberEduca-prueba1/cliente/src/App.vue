<template>
  <div id="app">
    
    <img src="" alt="">

    <router-view/>
    
    <footer>
      
    </footer>
  </div>
</template>
<script>
import Navegador from "@/components/nav.vue"; // Asegúrate de que la ruta sea correcta

export default {
  components: {
    Navegador, // Registra el componente de navegación para su uso en la plantilla
  },mounted(){
    //localStorage.clear();
  }
  
};

</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}





</style>
