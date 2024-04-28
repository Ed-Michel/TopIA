<template>
  <div id="contenedorForm">

    <div id = "modulologin">
        <h1>Iniciar Sesión</h1>
        <!--  
        <form @submit.prevent="login">
        <label for="username">Username:</label>
        <input v-model="username" type="text" id="username" required>
  
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" required>
      Esto es un comentario en el template Vue 
        <button type="submit">Login</button>
        <button type="submit" @click.prevent = redireccionar()>PRUEBA</button>
      </form>-->

        <form id="login-form">
          <label for="email" class="sr-only">Email</label>
          <input v-model="email" type="email" name="email" id="email" placeholder="Correo electrónico">
          <label for="contrasena" class="sr-only">Contraseña</label>
          <input v-model = contrasena type="password" name="contrasena" id="contrasena" placeholder="Contraseña">
          <button type="input" @click.prevent="login()">Iniciar Sesión</button>
          <p class="error escondido">Error al iniciar sesión</p>
        </form>
        <p>¿Todavía no tienes una cuenta? - <a href="/registro">Registrate</a></p>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
import {URL_DATOS} from '../../utils/constantes'
import { mapActions, mapGetters } from 'vuex';
import authService from '../../utils/authService';
export default {
  data() {
    return {
      email: '',
      contrasena: ''
    };
  },
  methods: {
    ...mapActions('userStore', ['loginUser']),
    async login() {
      try {
        /*const response = await axios.post('http://your-backend-api/login', {
          username: this.username,
          password: this.password
        });*/

        // Store the received token securely (e.g., in local storage)
        //localStorage.setItem('token', response.data.token);

        // Set authentication status in Vuex or other global state management
        //this.$store.commit('setLoggedIn', true);
        /*
        const response = await axios.post(URL_DATOS+'api/login', {
          EMAIL: this.email,
          CONTRASENIA: this.contrasena
        });
        localStorage.setItem("token",response.data.token)
       

        const userData = {
        email: this.email,
        password: this.contrasena
      };
      this.loginUser(userData);
      */
      try {
        await authService.login(this.email, this.contrasena);
        localStorage.setItem("email",this.email )
        this.$router.push('/Home');
        this.$store.dispatch('login');
        console.log('Logged in successfully');
      } catch (error) {
        console.error('Login failed:', error.message);
        // Handle login error
      }


      
      } catch (error) {
        console.error('Login failed:', error);
      }
    },
    redireccionar() {
      // Usa this.$router.push para redirigir a una nueva página
     
      //this.$store.commit('cambiarOpcionesMenu');
    }
      
    },
  };
</script>
<style>
/* Puedes enlazar el archivo CSS externo así: */
@import url('../../assets/login.css');
</style>