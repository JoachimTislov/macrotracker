<script setup lang="ts">
import { showAlert, alertMessage, alertClassName } from '@/logic/initVariables'

function hideAlert() {
  showAlert.value = false
}
</script>

<template>
  <div v-if="showAlert" ref="alertBox" :class="alertClassName" class="mb-3 alert">
    <button type="button" class="btn btn-md float-end" @click.prevent="hideAlert">
      <font-awesome-icon :icon="['fas', 'x']" />
    </button>

    <h4>
      <strong> {{ alertMessage }} </strong>
    </h4>
  </div>
</template>

<style scoped>
button {
  color: white;
}

h4 {
  color: rgb(236, 223, 223);
  font-size: clamp(1.1rem, 2.5vw, 1.5rem);

  margin-top: 0.3rem;
}

div {
  position: -webkit-sticky;
  position: sticky;
  top: 5px;
  z-index: 10;
}

@keyframes alert {
  0% {
    transform: translateY(-10px);
  }

  100% {
    transform: translateY(0);
  }
}

.smoothIn {
  animation: alert 0.5s;
}
</style>
