<script setup lang="ts">
import { checkValidationArr } from '@/logic/checkLogic/checkValidationArr'
import { fetchResource } from '@/logic/Ajax/ajax'
import { getFormDataInJSONFormat } from '@/logic/Ajax/get/getFormDataInJSONFormat'
import { getIngredients } from '@/logic/Ajax/get/getIngredients'
import type { Ingredient } from '@/logic/types'
import { ref, watch } from 'vue'
import AlertBox from './AlertBox.vue'
import { _alert, alertDanger, hideAlert } from '@/logic/alertFunctions'
import IngredientInputModule from './IngredientInputModule.vue'
import {
  createOrEdit_ingredient_validation_arr,
  fetchingResource
} from '@/logic/initVariables'
import { getMeals } from '@/logic/Ajax/get/getMeals'
import RequestLoader from '../RequestLoader.vue'
import { randomNumber } from '@/logic/randomNumber'

const props = defineProps<{
  formulate_type: string
  ingredient?: Ingredient
}>()

const http_method = ref<string>('POST')
const url = ref<string>('/ingredient')
const modal_id = `${props.formulate_type}_ingredient_modal`

const _formulate_type = ref<string>('Create')

watch(
  () => props.ingredient,
  (newIngredient) => {
    if (newIngredient) {
      _formulate_type.value = 'Edit'
      http_method.value = 'PUT'
      url.value = `/ingredient/${newIngredient.ingredient_id}`
    }
  }
)

async function IngredientEvent() {
  if (checkValidationArr(createOrEdit_ingredient_validation_arr)) {
    const json = getFormDataInJSONFormat(`${props.formulate_type}_ingredient_form`)
    const response = await fetchResource(http_method.value, json, url.value, 'token', modal_id)

    if (response && response.ok) {
      await getIngredients()
      await getMeals()
    }
  } else {
    alertDanger()
    await _alert("Fill out the required fields: 'Name' and 'Amount'. Nutrient values may be zero.")
  }
}
</script>

<template>
  <div class="modal modal-sm fade Modal" :id="modal_id">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title mr-2">{{ _formulate_type }} Ingredient:</h4>
          <button class="btn btn-lg ms-auto" @click="hideAlert()" data-bs-dismiss="modal">
            <font-awesome-icon :icon="['fas', 'x']" />
          </button>
        </div>

        <div class="modal-body">
          <AlertBox />

          <form :id="`${props.formulate_type}_ingredient_form`">
            <IngredientInputModule :random="randomNumber" :ingredient="ingredient" food_type="ingredient" />
          </form>
        </div>
        <div class="modal-footer">
          <div v-if="fetchingResource">
            <RequestLoader />
          </div>
          <button :disabled="fetchingResource" type="submit" @click="IngredientEvent()" class="btn btn-success btn-lg">
            {{ _formulate_type }}
            Ingredient
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
