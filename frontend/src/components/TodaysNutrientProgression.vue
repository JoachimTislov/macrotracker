<script setup lang="ts">
import {
  eaten_nutrient_progression,
  fetchingResource,
  userInfo
} from '@/logic/initVariables'

import RadialBar from './RadialBar.vue'
import RequestLoader from './RequestLoader.vue'

const calorieChartOptions = {
  chart: {
    foreColor: '#fff'
  },
  plotOptions: {
    radialBar: {
      hollow: {
        margin: 0,
        size: '70%',
        background: '#212121'
      },
      dataLabels: {
        showOn: 'always',
        name: {
          offsetY: -10,
          fontSize: 'clamp(1.5rem, 2vw, 2rem)'
        },
        value: {
          offsetX: -3,
          fontSize: 'clamp(1.5rem, 2vw, 2rem)',
          padding: '20px'
        }
      }
    }
  },
  stroke: {
    linecap: 'round'
  },
  labels: ['Calories']
}
</script>

<template>
  <header class="card-header p-3">
    <h4>Todays nutrient progression</h4>
  </header>
  <div v-if="fetchingResource && !userInfo" class="m-2 d-flex">
    <h4>Calculating data..</h4>
    <RequestLoader />
  </div>
  <section class="d-flex flex-wrap justify-content-center" style="width: 100%">
    <div class="d-flex align-items-center">
      <apexchart style="width: clamp(250px, 35vw, 450px)" type="radialBar"
        :series="eaten_nutrient_progression['calories']" :options="calorieChartOptions">
      </apexchart>
    </div>

    <div class="d-flex flex-column">
      <div class="d-flex flex-wrap justify-content-center" v-for="(entry, index) in [
        ['protein', 'fat'],
        ['carbohydrates', 'sugar']
      ]" :key="index">
        <div v-for="nutrient in entry" :key="nutrient">
          <RadialBar style="width: clamp(174px, 25vw, 300px)" :series="eaten_nutrient_progression[nutrient]"
            :label="nutrient.charAt(0).toLocaleUpperCase() + nutrient.slice(1)" />
        </div>
      </div>
    </div>
  </section>
</template>
