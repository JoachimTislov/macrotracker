<script setup lang="ts">
import {
  calender_data,
  selected_end_date,
  selected_start_date
} from '@/logic/initVariables'
import { structureCalenderData } from '@/logic/structure_calender_data'

const props = defineProps<{
  calc_nutrient_stats_for_given_period?: () => void
}>()

function handleChangedDateEvent(identifier: string) {
  if (calender_data.value) structureCalenderData(identifier)

  if (props.calc_nutrient_stats_for_given_period) {
    props.calc_nutrient_stats_for_given_period()
  }
}
</script>

<template>
  <div class="d-flex align-items-center">
    <label for="start" class="me-2"> Start: </label>
    <input name="start" type="date" class="form-control form-control-md" v-model="selected_start_date"
      @change="handleChangedDateEvent('start')" />
  </div>
  <div class="d-flex align-items-center mt-1">
    <label for="end" class="me-3"> End: </label>
    <input name="end" type="date" class="form-control form-control-md" v-model="selected_end_date"
      @change="handleChangedDateEvent('end')" />
  </div>
</template>
