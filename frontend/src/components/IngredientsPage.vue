<script setup lang="ts">
import { deleteEntity } from '@/logic/Ajax/ajax'
import { ingredients, fetchingResource } from '@/logic/initVariables'
import type { Ingredient, IngredientModal } from '@/logic/types'
import { computed, onMounted, reactive, ref } from 'vue'
import { CAccordion, CAccordionItem, CAccordionHeader, CAccordionBody } from '@coreui/vue'
import { getIngredients } from '@/logic/Ajax/get/getIngredients'
import { splitArrayWithRespectToSortedArray } from '@/logic/splitArrayWithRespectToSortedArray'
import { checkFilterForArray } from '@/logic/checkLogic/checkFilterForArray'
import FormulateIngredient from './Modules/FormulateIngredient.vue'
import AlertBox from './Modules/AlertBox.vue'
import { hideAlert } from '@/logic/alertFunctions'
import RequestLoader from './RequestLoader.vue'
import { changeValidationForNameAndAmount } from '@/logic/validation'

onMounted(async () => {
  await getIngredients()
})

const storedSortValue = localStorage.getItem('meal_sort_value')
const sort_value = ref<string>(storedSortValue ? storedSortValue : 'Sort by')
const search_value = ref<string>('')

const ingredientModalInformation: IngredientModal = reactive({
  Create: {
    formulate_type: 'create'
  },
  Edit: {
    formulate_type: 'edit',
    ingredient: undefined
  }
})

function handleEditEvent(ingredient: Ingredient) {
  hideAlert()
  changeValidationForNameAndAmount(true)
  ingredientModalInformation.Edit.ingredient = ingredient
}

function handleCreateIngredientEvent() {
  hideAlert()
  changeValidationForNameAndAmount(false)
}

const list_of_ingredients = computed(() => {
  return splitArrayWithRespectToSortedArray(
    checkFilterForArray(ingredients.value, search_value.value, sort_value.value)
  )
})
</script>

<template>
  <template v-for="(ingredientModal, index) in ingredientModalInformation" :key="index">
    <FormulateIngredient :formulate_type="ingredientModal.formulate_type" :ingredient="ingredientModal.ingredient" />
  </template>

  <section class="card">
    <div class="card-header">
      <h2 class="m-0">Your ingredients</h2>

      <div class="d-flex flex-wrap">
        <div class="m-2 input-group" style="min-width: 150px; max-width: 500px">
          <input class="form-control form-control-lg" type="text" placeholder="Search" v-model="search_value" />

          <select class="form-control form-control-lg" @change="search_value = ''" v-model="sort_value">
            <option disabled selected>Sort by</option>
            <option value="name">Name</option>
            <option value="protein">Protein</option>
            <option value="calories">Calories</option>
            <option value="carbohydrates">Carbohydrates</option>
            <option value="fat">Fat</option>
            <option value="sugar">Sugar</option>
          </select>
        </div>

        <button type="button" class="m-2 btn-success btn btn-lg" data-bs-toggle="modal"
          data-bs-target="#create_ingredient_modal" @click="handleCreateIngredientEvent()">
          Create ingredient
        </button>
      </div>
    </div>

    <div class="card-body">
      <AlertBox />

      <template v-if="fetchingResource && !ingredients">
        <div class="d-flex justify-content-center">
          <RequestLoader />
        </div>
      </template>

      <template v-else>
        <div class="ingredientsList">
          <div v-for="(ingredientChunk, index) in list_of_ingredients" :key="index" style="width: 100%">
            <CAccordion flush>
              <CAccordionItem v-for="ingredient in ingredientChunk" :id="'ingredient' + ingredient['ingredient_id']"
                :key="ingredient.ingredient_id" class="border border-3 border-secondary">
                <CAccordionHeader>
                  <h4>{{ ingredient['name'] }}</h4>
                </CAccordionHeader>
                <CAccordionBody>
                  <ul class="list-group">
                    <li class="list-group-item">Amount: {{ ingredient['amount'] }}</li>
                    <li class="list-group-item">Protein: {{ ingredient['protein'] }}g</li>
                    <li class="list-group-item">Calories: {{ ingredient['calories'] }}kcal</li>
                    <li class="list-group-item">
                      Carbohydrates: {{ ingredient['carbohydrates'] }}g
                    </li>
                    <li class="list-group-item">Fat: {{ ingredient['fat'] }}g</li>
                    <li class="list-group-item">Sugar: {{ ingredient['sugar'] }}g</li>
                  </ul>

                  <div class="d-flex btn-group mt-2">
                    <button type="button" class="btn btn-info" @click="handleEditEvent(ingredient)"
                      data-bs-toggle="modal" data-bs-target="#edit_ingredient_modal">
                      Edit <font-awesome-icon :icon="['fas', 'pen-to-square']" />
                    </button>
                    <button type="button" @click="
                      deleteEntity(`/ingredient/${ingredient['ingredient_id']}`, getIngredients)
                      " class="btn btn-danger">
                      Delete <font-awesome-icon :icon="['fas', 'trash']" />
                    </button>
                  </div>
                </CAccordionBody>
              </CAccordionItem>
            </CAccordion>
          </div>
        </div>
        <div v-if="list_of_ingredients[0].length == 0" class="ml-5 mb-2 mt-2">
          <h4 v-if="search_value == ''">You don't have any ingredients</h4>
          <h4 v-if="search_value != ''">
            You don't have any ingredients with name: {{ search_value }}
          </h4>

          <button type="button" class="btn-success btn btn-md" data-bs-toggle="modal"
            data-bs-target="#create_ingredient_modal" @click="handleCreateIngredientEvent()">
            Create ingredient
          </button>
        </div>
      </template>
    </div>
  </section>
</template>

<style scoped>
.ingredientsList {
  display: flex;
  flex-direction: row;

  justify-content: center;
}

@media (max-width: 766px) {
  .ingredientsList {
    flex-direction: column;
  }
}
</style>
