<template>
  <div class="aaa">
    <custom-story :scenes="scenes" />
  </div>
</template>

<script>
import CustomStory from './CustomStory.vue';
import FirstSceneComponent from './Escena1.vue';
import SecondSceneComponent from './Escena2.vue';

export default {
  components: {
    CustomStory
  },
  data() {
    return {
      scenes: [
        {
          component: FirstSceneComponent
        },
        {
          component: SecondSceneComponent
        }
      ]
    };
  }
};
</script>

<style scoped>
.app {
  text-align: center;
}
</style>