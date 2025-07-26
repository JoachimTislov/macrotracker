<script setup lang="ts">
import type { Form_configuration, Ingredient } from '@/logic/types'
import { reactive, watch } from 'vue'
import IngredientBlueprint from './IngredientBlueprint.vue'

const props = defineProps<{
  food_type: string
  ingredient?: Ingredient
  index?: number
  random: number
}>()

const i = props.ingredient

const form_configurations: Form_configuration = reactive([
  {
    class: 'form-group',
    identifier: 'Name',
    validation_type: 'Name',
    inputType: 'text',
    value: i ? i.name : ''
  },
  {
    class: 'form-group',
    identifier: 'Amount',
    validation_type: 'Amount',
    inputType: 'text',
    value: i ? i.amount : 0
  },
  {
    class: 'input-group',
    identifier: 'Calories',
    validation_type: 'Nutrient',
    inputType: 'number',
    value: i ? i.calories : 0,
    unit: 'kcal'
  },
  {
    class: 'input-group',
    identifier: 'Carbohydrates',
    validation_type: 'Nutrient',
    inputType: 'number',
    value: i ? i.carbohydrates : 0,
    unit: 'g'
  },
  {
    class: 'input-group',
    identifier: 'Fat',
    validation_type: 'Nutrient',
    inputType: 'number',
    value: i ? i.fat : 0,
    unit: 'g'
  },
  {
    class: 'input-group',
    identifier: 'Protein',
    validation_type: 'Nutrient',
    inputType: 'number',
    value: i ? i.protein : 0,
    unit: 'g'
  },
  {
    class: 'input-group',
    identifier: 'Sugar',
    validation_type: 'Nutrient',
    inputType: 'number',
    value: i ? i.sugar : 0,
    unit: 'g'
  }
])

watch(
  () => props.ingredient,
  (newIngredient) => {
    if (newIngredient) {
      for (const configuration of form_configurations) {
        const key = configuration.identifier.toLocaleLowerCase()
        const value = newIngredient[key]
        if (value) configuration.value = value
      }
    }
  }
)
</script>

<template>
  <template v-for="entry in form_configurations" :key="entry.identifier">
    <IngredientBlueprint :ingredient-info="entry" :food_type="food_type" :index="index" :random="random" />
  </template>
</template>
