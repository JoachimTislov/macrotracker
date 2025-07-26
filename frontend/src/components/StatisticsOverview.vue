<script setup lang="ts">
import { onMounted } from 'vue'
import { getUserInfo } from '@/logic/Ajax/get/getUserInfo'
import {
  calcNutrientStatsForGivenPeriod,
  setupNutrientProgressChartsData
} from '@/logic/statisticsFunctions'
import { get_calender_data } from '@/logic/Ajax/get/get_calender_data'
import {
  stats_for_dates,
  StatsToShow,
  selected_start_date,
  selected_end_date,
  overall_stats,
  fetchingResource,
  calender_data
} from '@/logic/initVariables'
import { getDayForDate, reverseInputDateFormat } from '@/logic/dateSystem'
import StartEndInput from './StartEndInput.vue'
import TodaysNutrientProgression from './TodaysNutrientProgression.vue'
import OverallStatsDonut from './OverallStatsDonut.vue'
import BarChart from './BarChart.vue'
import RequestLoader from './RequestLoader.vue'

onMounted(async () => {
  await getUserInfo()
  await get_calender_data()

  setupNutrientProgressChartsData()
  calcNutrientStatsForGivenPeriod()
})
</script>

<template>
  <section class="card mb-2">
    <TodaysNutrientProgression />

    <header class="card-header p-3 d-flex">
      <div class="d-flex flex-column">
        <h3 class="m-2">
          Statistics
          <p>Total, average and nutrient stats for each meal</p>
        </h3>
        <div class="d-flex flex-column m-3 mt-0" style="width: 200px">
          <StartEndInput :calc_nutrient_stats_for_given_period="calcNutrientStatsForGivenPeriod" />
        </div>
      </div>
    </header>
    <section class="card-body">
      <template v-if="fetchingResource && calender_data && Object.keys(calender_data).length == 0">
        <div class="d-flex justify-content-center">
          <RequestLoader />
        </div>
      </template>

      <template v-else>
        <template v-if="StatsToShow">
          <div class="border border-3 rounded p-3">
            <h4>
              Overall:
              <template v-if="selected_start_date == selected_end_date">
                {{ reverseInputDateFormat(selected_start_date) }}
              </template>
              <template v-else>
                {{ reverseInputDateFormat(selected_start_date) }} -
                {{ reverseInputDateFormat(selected_end_date) }}
              </template>
            </h4>

            <OverallStatsDonut :stats="overall_stats" />
          </div>

          <div class="mt-2" v-for="(date, index) in Object.keys(stats_for_dates)" :key="index">
            <div class="card-header">
              <h5 class="mt-2">{{ getDayForDate(date) }} {{ date }}</h5>
            </div>
            <template v-if="Object.keys(stats_for_dates).length != 1">
              <OverallStatsDonut :stats="{
                total: stats_for_dates[date].total,
                average: stats_for_dates[date].average
              }" />
            </template>

            <div class="m-4 ms-0" v-for="(meal_name, index) in Object.keys(stats_for_dates[date].meals)" :key="index">
              <BarChart :data="stats_for_dates[date].meals[meal_name].data" :name="meal_name" />
            </div>
          </div>
        </template>

        <template v-else>
          <h4 class="ms-2">
            No data to visualize, add meals to your calender inside of given period to view
            statistics
          </h4>
        </template>
      </template>
    </section>
  </section>
</template>

<style scoped>
.donutContainer {
  width: clamp(300px, 40vw, 500px);
}

.nutrient-container {
  flex: 1;
  min-width: clamp(200px, 10vw, 500px);
}

h4 {
  font-size: clamp(0.9rem, 1vw, 1.5rem);
}
</style>
