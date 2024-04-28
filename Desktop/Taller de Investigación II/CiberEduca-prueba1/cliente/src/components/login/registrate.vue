<template>
    <div id="contenedorForm">
        <div id="moduloregistro">
            <h1>¡Registrate ahora!</h1>
            <!--
            <label for="text" class="sr-only">Nombre</label>
            <input type="text" name="nombre" id="nombre" placeholder="Nombre">
            <label for="text" class="sr-only">Apellido Paterno</label>
            <input type="text" name="apellidoPat" id="apellidoPat" placeholder="Apellido Paterno">
            <label for="text" class="sr-only">Apellido Materno</label>
            <input type="text" name="apellidoMat" id="apellidoMat" placeholder="Apellido Materno">
            -->
            <form id="registro-form">
                <label for="email" class="sr-only" >Email</label>
                <input type="email" name="email" id="email" placeholder="Correo electrónico" v-model="usuarios.EMAIL">
                <label for="contrasena" class="sr-only">Contraseña</label>
                <input type="password" name="contrasena" id="contrasena" placeholder="Contraseña" v-model="usuarios.CONTRASENIA">
                <button type="input" @click.prevent="nuevo()">Registrarse</button>
                <p class="error escondido">Error al registrarse</p>
            </form>
            <p>¿Ya tienes una cuenta? - <a href="/login">Iniciar Sesión</a></p>
        </div>
    </div>
</template>
    
<script>

import { URL_DATOS } from '@/utils/constantes';
import axios from 'axios';
export default {
    data() {
        return {
            usuarios:[],
        };
    },
    methods: {
        nuevo: async function(){
            const res = await axios.post(URL_DATOS + "auth/register", {
                EMAIL: this.usuarios.EMAIL,
                CONTRASENIA: this.usuarios.CONTRASENIA,
            });
        }
    }
}
</script>
<style scoped>
@import url('../../assets/login.css');
</style>