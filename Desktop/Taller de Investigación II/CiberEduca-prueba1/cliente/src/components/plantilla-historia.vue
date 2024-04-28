<template>


  <div class="custom-story">
    <!-- Contenido de la escena actual -->
    <div class="story-content">
      <!-- Contenido de la escena actual -->
      <slot :scene="scenes[currentIndex]">
        <div :class="getSceneClasses(scenes[currentIndex])">
          <h1>{{ scenes[currentIndex].title }}</h1>
          <p>{{ scenes[currentIndex].description }}</p>
          <!-- Renderizar imagen si está presente en la escena -->
          <img v-if="scenes[currentIndex].image" :src="scenes[currentIndex].image" alt="Imagen de la escena" />
        </div>
      </slot>
    </div>

    <div class="story-controls">
      <button @click="goToPrevious" :disabled="currentIndex === 0" class="prev-button">Anterior</button>
      <button @click="goToNext" :disabled="currentIndex === scenes.length - 1" class="next-button">Siguiente</button>
    </div>

  </div>
</template>

<script>
export default {
  props: {
    scenes: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      currentIndex: 0,
    };
  },
  methods: {
    goToPrevious() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    },
    goToNext() {
      if (this.currentIndex < this.scenes.length - 1) {
        this.currentIndex++;
      }
    },
    getSceneClasses(scene) {
      // Lógica para obtener las clases de la escena actual
      const classes = ['custom-scene'];

      if (scene.isFirstScene) {
        classes.push('first-scene');
      }

      // Puedes agregar lógica adicional aquí para otras clases según tus necesidades

      return classes;
    },
  },
};
</script>

<style scoped>
/* Estilos generales para el componente */
.custom-story {
  position: relative;
}

/* Estilos para el contenido de la historia */
.story-content {
  margin-bottom: 20px;
  /* Espacio entre el contenido y los botones de control */
}

/* Estilos para los botones de control */
.story-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.prev-button,
.next-button {
  padding: 10px;
  margin: 0 10px;
}

/* Puedes agregar estilos adicionales aquí si es necesario */
</style>