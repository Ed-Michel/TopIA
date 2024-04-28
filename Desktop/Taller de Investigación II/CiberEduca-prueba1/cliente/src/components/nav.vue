<template>
    <div>
      <nav>
        <router-link v-for="option in menuOptions" :key="option.name" :to="option.to">
          {{ option.label }}
        </router-link>
      <img src="../assets/logo.png" alt="">
      </nav>
    </div>
  </template>
  
  <script>
  export default {
    computed: {
      menuOptions() {
        const options = this.$store.state.menuOptions || [];
      console.log('menuOptions:', options);
      return options;
        //return this.$store.state.menuOptions ;
      },
    },
  };
  </script>
  
  <style>
  nav {
    background: #222A59;
    display: flex;
    justify-content: space-between;
    align-items: center;  

    img {
      width: 50px;
      margin-left: auto;  
    }

    a {
      font-weight: bold;
      color: #D989BD;
      padding: 30px;
      vertical-align: middle;

      &.router-link-exact-active {
        color: #F22222;
      }
    }
  }
</style>