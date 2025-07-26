<script setup lang="ts">
import { labels } from '@/logic/initVariables'
import DonutChart from './DonutChart.vue'

defineProps<{
  stats: {
    total: number[]
    average: number[]
  }
}>()
</script>

<template>
  <div class="d-flex flex-wrap justify-content-center">
    <div class="p-3 m-1 donutContainer">
      <h4>Total</h4>

      <DonutChart :labels="labels" :series="stats.total" />
    </div>

    <div class="p-3 m-1 donutContainer">
      <h4>Average</h4>
      <DonutChart :labels="labels" :series="stats.average" />
    </div>
  </div>
</template>

<style scoped>
.donutContainer {
  width: clamp(300px, 35vw, 500px);
}
</style>
