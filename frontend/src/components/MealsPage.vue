<script setup lang="ts">
import { fetchingResource, meal_name_validation, meals } from '@/logic/initVariables'
import { computed, onMounted, reactive, ref } from 'vue'
import { splitArrayWithRespectToSortedArray } from '@/logic/splitArrayWithRespectToSortedArray'
import { checkFilterForArray } from '@/logic/checkLogic/checkFilterForArray'
import { CAccordion, CAccordionItem, CAccordionHeader, CAccordionBody } from '@coreui/vue'
import { getMeals } from '@/logic/Ajax/get/getMeals'
import type { Meal_with_ingredients, mealModal } from '@/logic//types'
import AlertBox from './Modules/AlertBox.vue'
import { hideAlert } from '@/logic/alertFunctions'
import FormulateMeal from './Modules/FormulateMeal.vue'
import { deleteEntity } from '@/logic/Ajax/ajax'
import RequestLoader from './RequestLoader.vue'
import { generateRandomNumber, randomNumber } from '@/logic/randomNumber'

onMounted(async () => {
  await getMeals()
})

const storedSortValue = localStorage.getItem('meal_sort_value')
const sort_value = ref<string>(storedSortValue ? storedSortValue : 'Sort by')
const search_value = ref<string>('')

const list_of_meals = computed(() => {
  return splitArrayWithRespectToSortedArray(
    checkFilterForArray(meals.value, search_value.value, sort_value.value)
  )
})

function createMeal() {
  hideAlert()
  changeMealNameValidation(false)

  generateRandomNumber()
}

const mealModalInformation: mealModal = reactive({
  Create: {
    formulate_type: 'create'
  },
  Edit: {
    formulate_type: 'edit',
    meal: undefined
  }
})

function changeMealNameValidation(value: boolean) {
  meal_name_validation.value = value
}

function editMeal(meal: Meal_with_ingredients) {
  hideAlert()
  changeMealNameValidation(true)
  mealModalInformation.Edit.meal = meal

  generateRandomNumber()

  // Assigning the respected meal id to the ingredient
  // Later to separate from ingredients which aren't added to the meal
  for (const ingredient of meal.ingredients) {
    ingredient.meal_id = meal.meal_id
  }
}
</script>

<template>
  <template v-for="mealModal in mealModalInformation" :key="mealModal.formulate_type">
    <FormulateMeal :formulate_type="mealModal.formulate_type" :meal="mealModal.meal" :random="randomNumber" />
  </template>

  <section class="card">
    <div class="card-header">
      <h2 class="m-0">Your meals</h2>

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

        <button class="m-2 create_button btn-success btn btn-lg" data-bs-toggle="modal"
          data-bs-target="#create_meal_modal" @click="createMeal()">
          Create a meal
        </button>
      </div>
    </div>

    <div class="card-body">
      <AlertBox />

      <template v-if="fetchingResource && !meals">
        <div class="d-flex justify-content-center">
          <RequestLoader />
        </div>
      </template>

      <template v-else>
        <div class="mealsList">
          <div v-for="(mealChunk, index) in list_of_meals" :key="index" style="width: 100%">
            <CAccordion flush>
              <CAccordionItem v-for="meal in mealChunk" :id="`meal-${meal['meal_id']}`" :key="meal['meal_id']"
                class="m-2 mt-0 border border-3 border-secondary">
                <CAccordionHeader>
                  <h4>{{ meal['name'] }}</h4>
                </CAccordionHeader>
                <CAccordionBody>
                  <template v-if="meal.ingredients.length > 1">
                    <label for="total_macros"> Total Macros </label>
                    <div class="d-flex flex-wrap" id="total_macros">
                      <small class="rounded border border-1 p-2 m-1">Protein: {{ meal['protein'] }}g</small>
                      <small class="rounded border border-1 p-2 m-1">Calories: {{ meal['calories'] }}kcal</small>
                      <small class="rounded border border-1 p-2 m-1">Carbohydrates: {{ meal['carbohydrates'] }}g</small>
                      <small class="rounded border border-1 p-2 m-1">Fat: {{ meal['fat'] }}g</small>
                      <small class="rounded border border-1 p-2 m-1">Sugar: {{ meal['sugar'] }}g</small>
                    </div>
                  </template>

                  <h5 v-if="meal['ingredients'].length > 0">Ingredients:</h5>
                  <div class="wrap">
                    <template v-if="meal['ingredients'].length > 0">
                      <div class="m-1" v-for="ingredient in meal['ingredients']" :key="ingredient['name']">
                        <ul class="list-group">
                          <li class="list-group-item list-group-item-info mr-3">
                            {{ ingredient['name'] }}
                          </li>
                          <li class="list-group-item">Amount: {{ ingredient['amount'] }}</li>
                          <li class="list-group-item mr-3">
                            Protein: {{ ingredient['protein'] }}g
                          </li>
                          <li class="list-group-item mr-3">
                            Calories: {{ ingredient['calories'] }}kcal
                          </li>
                          <li class="list-group-item mr-3">
                            Carbohydrates: {{ ingredient['carbohydrates'] }}g
                          </li>
                          <li class="list-group-item mr-3">Fat: {{ ingredient['fat'] }}g</li>
                          <li class="list-group-item mr-3">Sugar: {{ ingredient['sugar'] }}g</li>
                        </ul>
                      </div>
                    </template>
                    <div v-if="meal['ingredients'].length == 0" class="mt-2">
                      <h5>{{ meal['name'] }} has zero ingredients</h5>
                    </div>
                  </div>

                  <div class="d-flex mt-2 btn-group btn-group-md">
                    <button class="btn-danger btn" @click="deleteEntity(`/meal/${meal['meal_id']}`, getMeals)">
                      Delete
                      <font-awesome-icon :icon="['fas', 'trash']" />
                    </button>
                    <button class="btn-primary btn" data-bs-toggle="modal" data-bs-target="#edit_meal_modal"
                      @click="editMeal(meal)">
                      Edit
                      <font-awesome-icon :icon="['fas', 'pen-to-square']" />
                    </button>
                  </div>
                </CAccordionBody>
              </CAccordionItem>
            </CAccordion>
          </div>
        </div>

        <div v-if="list_of_meals[0].length == 0" class="ml-5 mb-2 mt-2">
          <h4 v-if="search_value == ''">You don't have any meals</h4>
          <h4 v-if="search_value != ''">You don't have any meals with name: {{ search_value }}</h4>
          <button type="button" class="btn-success btn btn-lg ml-2" data-bs-toggle="modal"
            data-bs-target="#create_meal_modal" @click="hideAlert(), createMeal()">
            <h5>Create a meal</h5>
          </button>
        </div>
      </template>
    </div>
  </section>
</template>

<style scoped>
.mealsList {
  display: flex;
  flex-direction: row;

  justify-content: center;
}

@media (max-width: 1000px) {
  .mealsList {
    flex-direction: column;
  }
}
</style>
