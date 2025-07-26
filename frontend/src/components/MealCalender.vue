<script setup lang="ts">
import {
  meals_for_time_of_day,
  selected_end_date,
  selected_start_date,
  zero_meals_for_time_period
} from '@/logic/initVariables'
import { onMounted } from 'vue'
import { getDayForDate, reverseInputDateFormat } from '@/logic/dateSystem'
import SelectMeal from './selectMeal.vue'
import { hideAlert } from '@/logic/alertFunctions'
import { deleteEntity } from '@/logic/Ajax/ajax'
import { get_calender_data } from '@/logic/Ajax/get/get_calender_data'
import StartEndInput from './StartEndInput.vue'
import type { Meals_for_time_of_day } from '@/logic/types'
import AlertBox from './Modules/AlertBox.vue'

onMounted(async () => {
  await get_calender_data()
})
</script>

<template>
  <AlertBox />

  <SelectMeal />

  <section class="card" id="meals_for_given_date">
    <div class="card-header d-flex flex-wrap">
      <div class="d-flex flex-column">
        <h2 class="mt-1">Meal Calender</h2>
        <div class="d-flex flex-column m-2">
          <StartEndInput />
        </div>
      </div>
      <div class="m-2 mt-2 me-auto">
        <button class="btn-success btn btn-md" data-bs-toggle="modal" data-bs-target="#select_meal_modal"
          @click="hideAlert()">
          Add a meal to the calender
        </button>
      </div>
    </div>

    <div class="card-body">
      <template v-if="zero_meals_for_time_period">
        <h4>
          There aren't meals in the calender between
          {{ reverseInputDateFormat(selected_start_date) }} and
          {{ reverseInputDateFormat(selected_end_date) }}
        </h4>
      </template>
      <template v-else v-for="(date, index) in Object.keys(meals_for_time_of_day)" :key="index">
        <div class="card-header">
          <h5 class="mt-2">{{ getDayForDate(date) }} {{ date }}</h5>
        </div>
        <div v-if="!(meals_for_time_of_day as Meals_for_time_of_day)[date].zero_meals_to_show" class="d-flex flex-wrap">
          <div v-for="(meals_for_given_time, meal_time) in (
            meals_for_time_of_day as Meals_for_time_of_day
          )[date].meal_periods" :key="meal_time">
            <ul v-if="meals_for_given_time.length > 0" class="list-group m-3">
              <li class="list-group-item list-group-item-secondary">
                <h4>{{ meal_time }}</h4>
              </li>

              <li class="list-group-item" v-for="(item, index) in meals_for_given_time" :key="index"
                :id="`calender_meal_${item['calender_id']}`">
                <div class="mt-2 d-flex gap-5">
                  <div class="d-flex flex-column">
                    <h5 class="fw-bold">{{ item.meal.name }}</h5>
                    <h5>{{ item['time_of_day'] }}</h5>
                  </div>
                  <div class="ms-auto">
                    <button class="btn-danger btn btn-sm"
                      @click="deleteEntity('/calender/' + item['calender_id'], get_calender_data)">
                      <font-awesome-icon :icon="['fas', 'trash']" />
                    </button>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
        <div v-else>
          <h6 class="m-3">You have not eaten any meals this day</h6>
        </div>
      </template>
    </div>
  </section>
</template>
