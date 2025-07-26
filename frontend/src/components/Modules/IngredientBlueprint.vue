<script setup lang="ts">
import type { IngredientInfo } from '@/logic/types'
import { ValidateText } from '@/logic/validation'
import { onMounted, ref, watch } from 'vue'
import {
  createOrEdit_ingredient_validation_arr,
  meal_validation
} from '@/logic/initVariables'

const ingredient_validation = ref<HTMLElement | null>(null)
const input_element = ref<HTMLElement | null>(null)

onMounted(() => {
  input_element.value?.focus()
  ingredient_validation.value?.focus()
})

const props = defineProps<{
  ingredientInfo: IngredientInfo
  food_type: string
  index?: number
  random: number
}>()

watch(
  () => props.random,
  () => {
    if (ingredient_validation.value) {
      ingredient_validation.value.style.display = 'none'
    }

    if (input_element.value) {
      input_element.value.classList.remove('is-invalid')
      input_element.value.classList.remove('is-valid')
    }
  }
)

const inputClass = 'form-control form-control-md'

const validation_array =
  props.food_type == 'ingredient'
    ? createOrEdit_ingredient_validation_arr
    : props.index != undefined
      ? meal_validation.value[props.index]
      : {}

const ingredient_name =
  props.index || props.index == 0
    ? `${props.index}-${props.ingredientInfo.identifier.toLowerCase()}`
    : props.ingredientInfo.identifier.toLowerCase()

function validateNutrient(event: Event) {
  validation_array[props.ingredientInfo.identifier.toLocaleLowerCase()] = ValidateText(
    event,
    ingredient_validation.value,
    props.ingredientInfo.validation_type,
    inputClass
  )
}
</script>

<template>
  <label class="m-0 mt-1 form-label" :for="ingredient_name">
    {{ ingredientInfo.identifier }}:
  </label>
  <div :class="ingredientInfo.class">
    <input ref="input_element" @input="validateNutrient($event)" :class="inputClass" :name="ingredient_name"
      :type="ingredientInfo.inputType" step="any" :value="ingredientInfo.value" />
    <div v-if="ingredientInfo.unit" class="input-group-append">
      <span class="input-group-text"> {{ ingredientInfo.unit }} </span>
    </div>
  </div>

  <div ref="ingredient_validation" class="ml-2 invalid-feedback"></div>
</template>
