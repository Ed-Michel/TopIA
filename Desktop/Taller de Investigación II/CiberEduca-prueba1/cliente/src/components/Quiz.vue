<template>
    <div>
        <h2>{{ pregunta }}</h2>
        <ul>
            <li v-for="(opcion, index) in opciones" :key="index">
                <button @click="seleccionarRespuesta(opcion)" :class="{ 'selected': respuestaSeleccionada === opcion }">
                    {{ opcion }}
                </button>
            </li>
        </ul>
        
        <div v-if="mostrarResultado">
            <p v-if="mostrarResultado">¡Respuesta correcta!</p>
            <p v-else>Respuesta incorrecta. La respuesta correcta es: {{ opciones[respuestaCorrecta] }}</p>
        </div>
    </div>
</template>
  
<script>
export default {
    props: {
        pregunta: {
            type: String,
            required: true
        },
        opciones: {
            type: Array,
            required: true
        },
        respuestaCorrecta: {
            type: Number, // Puedes ajustar el tipo según tu necesidad
            required: true
        }
    },
    data() {
        return {
            respuestaSeleccionada: null,
            mostrarResultado: false
        };
    },
    methods: {
        verificarRespuesta() {
            this.mostrarResultado = true;
        },
        esRespuestaCorrecta() {
            console.log(this.respuestaSeleccionada === this.opciones[this.respuestaCorrecta])
            return this.respuestaSeleccionada === this.opciones[this.respuestaCorrecta]
        },
        seleccionarRespuesta(opcion) {
            this.respuestaSeleccionada =opcion
            this.mostrarResultado= this.esRespuestaCorrecta();

        },
    }
};
</script>
  
<style scoped>
/* Puedes agregar estilos aquí si lo necesitas */
</style>