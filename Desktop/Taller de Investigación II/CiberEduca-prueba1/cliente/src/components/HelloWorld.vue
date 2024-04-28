<template>
  <div class="hello">
    <Navegador/>
    <section id="seccPrincipal">
      <h1>Adentrate a CiberEduca</h1>
      <h2>Acerca de Nosotros</h2>
      <article id="art01" class="slide-right">
        <img src="../assets/gifs/dispositivos.gif" alt="">
        <p>CiberEduca es una aplicación web educativa donde aprenderás buenas prácticas para estár a salvo en las redes
          sociales. </p>
      </article>


      <h2>Que ofrecemos</h2>

      <article id="art02">
        <p>CiberEduca cuenta con actividades didacticas basadas en historias reales de usuarios que han sufrido algún
          ciber-delito como
          ciber-acoso, robo de identidad y
        </p>

        <img src="../assets/imgs/ciberdelitosProtegernos.png" alt="">
      </article>
<h2>Sigue tu progreso</h2>
      <article id="art03">
        
        <p>Vizualiza el progreso logrado de las actividades</p>
        <br>
        <div class="chart-container">
          <div class="bar" style="--progress: 70%;"></div>
          <div class="bar" style="--progress: 50%;"></div>
          <div class="bar" style="--progress: 80%;"></div>
        </div>
      </article>
    </section>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import Navegador from "./nav.vue"
export default {
  name: 'HelloWorld',
  components:{ Navegador}
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Puedes enlazar el archivo CSS externo así: */
@import url('../assets/helloworld.css');
</style>

