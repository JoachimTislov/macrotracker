<script setup lang="ts">
import Navbar from './components/NavbarPage.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="container mb-3">
    <Navbar />
    <RouterView />
  </div>
</template>
