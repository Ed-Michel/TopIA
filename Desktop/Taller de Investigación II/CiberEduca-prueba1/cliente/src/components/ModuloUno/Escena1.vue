<template>
  <div class="avatar-container" :style="{ top: avatarTop, left: avatarLeft }">
 
    <div class="dialogue-container" :class="{ 'show-dialogue': showDialogue }">
      <div class="dialogue">{{ currentDialogue }}</div>
    </div>
    <div class="avatar">
      <img src="../../assets/imgs/Policia.png" alt="" id="policia">
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      showDialogue: false,
      dialogues: ["Hola, ¿cómo estás?", 
      "Somos la policia Cibernetica, encargada de defender ", 
      
      "¡Qué bueno verte!", "Hasta luego."],
      currentDialogueIndex: 0,
      currentDialogue: "",
      avatarTop: "50%",
      avatarLeft: "50%"
    };
  },
  mounted() {
    setTimeout(() => {
      this.showDialogue = true;
      this.showNextDialogue();
      this.moveAvatar();
    }, 2000); // 2 segundos de retraso
  },
  methods: {
    showNextDialogue() {
      if (this.currentDialogueIndex < this.dialogues.length) {
        this.currentDialogue = this.dialogues[this.currentDialogueIndex];
        this.currentDialogueIndex++;
        setTimeout(this.showNextDialogue, 2000); // Mostrar el próximo diálogo después de 2 segundos
      } else {
        // Si se muestran todos los diálogos, ocultar el cuadro de diálogo
        setTimeout(() => {
          this.showDialogue = false;
        }, 2000);
      }
    },
    moveAvatar() {
      // Ejemplo de movimiento del avatar
      setInterval(() => {
        // Aquí puedes definir las posiciones de movimiento del avatar
        const newTop = Math.floor(Math.random() * 100) + "%"; // Posición aleatoria en vertical
        const newLeft = Math.floor(Math.random() * 100) + "%"; // Posición aleatoria en horizontal
        this.avatarTop = newTop;
        this.avatarLeft = newLeft;
      }, 3000); // Cambio de posición cada 3 segundos
    }
  }
}
</script>

<style scoped>
.avatar-container {
  position: relative;
  width: 200px; /* Ajusta el tamaño según sea necesario */
  height: 200px; /* Ajusta el tamaño según sea necesario */
}
/*
.avatar {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px; /* Ajusta el tamaño según sea necesario */
  height: 100px; /* Ajusta el tamaño según sea necesario */
  background-color: #ccc; /* Cambia el color del avatar según sea necesario */
  border-radius: 50%; /* Haz que el avatar sea redondo */
  /* Puedes agregar una imagen de fondo en lugar de un color */
  /* background-image: url('ruta/al/avatar.png'); */
  /* background-size: cover; 
}
*/
/* Estilos para el cuadro de diálogo */
.dialogue-container {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  background-color: white;
  padding: 10px;
  border-radius: 10px;
  opacity: 0;
  visibility: hidden; /* Ocultar inicialmente el diálogo */
}
#policia{
  height: 200px;
  width: 100px;
}
.show-dialogue {
  animation-name: aparecer-dialogo;
  animation-duration: 1s;
  animation-fill-mode: forwards;
  opacity: 1;
  visibility: visible;
}

/* Animación para mostrar el diálogo */
@keyframes aparecer-dialogo {
  from {
    opacity: 0;
    transform: translate(-50%, 20px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}


.avatar-container {
  position: relative;
  width: 200px;
  height: 200px;
}

.avatar-police {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 200px;
  background-color: #3d3d3d;
  border-radius: 5px;
}

.head {
  position: absolute;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 60px;
  background-color: #3d3d3d;
  border-radius: 50%;
}

.body {
  position: absolute;
  top: 30%;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 100px;
  background-color: #3d3d3d;
}

.badge {
  position: absolute;
  top: 12%;
  left: 30%;
  width: 30px;
  height: 30px;
  background-color: #ffa500;
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
}
</style>