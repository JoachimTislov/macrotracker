<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import AlertBox from './AlertBox.vue'
import { changeValidationForNameAndAmount, ValidateText } from '@/logic/validation'
import type {
  validation_Object,
  Ingredient,
  Ingredients,
  Meal_with_ingredients,
  Api_search_data
} from '@/logic/types'
import { hideModal } from '@/logic/hideModal'
import { _alert, alertDanger, alertSuccess, hideAlert } from '@/logic/alertFunctions'
import { getMeals } from '@/logic/Ajax/get/getMeals'
import { fetchResource } from '@/logic/Ajax/ajax'
import { getFormDataInJSONFormat } from '@/logic/Ajax/get/getFormDataInJSONFormat'
import { checkValidationArr } from '@/logic/checkLogic/checkValidationArr'
import {
  meal_name_validation,
  meal_validation,
  ingredients,
  ingredient_validation,
  fetchingResource
} from '@/logic/initVariables'
import FormulateIngredient from './FormulateIngredient.vue'
import IngredientInputModule from './IngredientInputModule.vue'
import { getIngredients } from '@/logic/Ajax/get/getIngredients'
import { deleteEntity } from '@/logic/Ajax/ajax'
import RequestLoader from '../RequestLoader.vue'
import { randomNumber } from '@/logic/randomNumber'
import deepClone from '@/logic/deepClone'

const meal_name_message_validation = ref<HTMLElement | null>(null)
const meal_name_input = ref<HTMLElement | null>(null)

onMounted(async () => {
  meal_name_message_validation.value?.focus()
  meal_name_input.value?.focus()
  await getIngredients()
})

const props = defineProps<{
  formulate_type: string
  meal?: Meal_with_ingredients
  random: number
}>()

const meal_name = ref<string>('')

const ingredientsData = ref<Ingredients>([])
const api_search_data = ref<Api_search_data | undefined>(undefined)

const http_method = ref<string>('POST')
const url = ref<string>('/meal')
const modal_id = `${props.formulate_type}_meal_modal`

const _formulate_type = ref<string>('Create')

watch(
  () => props.meal,
  (newMeal) => {
    const ingredientValidation = ref<validation_Object>(deepClone(ingredient_validation))

    if (newMeal) {
      _formulate_type.value = 'Edit'
      http_method.value = 'PUT'
      url.value = `/meal/${newMeal.meal_id}`

      meal_name.value = newMeal.name

      ingredientValidation.value.name = true
      ingredientValidation.value.amount = true

      // Deep copy, preventing unwanted features
      const copy = JSON.parse(JSON.stringify(newMeal.ingredients))
      ingredientsData.value = copy
    }
    meal_validation.value = []

    for (let i = 0; i < ingredientsData.value.length; i++) {
      meal_validation.value.push(ingredientValidation.value)
    }
  }
)

watch(
  () => props.random,
  () => {
    if (!props.meal) {
      meal_name.value = ''
      ingredientsData.value = []
    } else {
      meal_name.value = props.meal?.name
    }

    if (meal_name_message_validation.value) {
      meal_name_message_validation.value.style.display = 'none'
    }

    if (meal_name_input.value) {
      meal_name_input.value.classList.remove('is-invalid')
      meal_name_input.value.classList.remove('is-valid')
    }
  }
)

function check_meal_validation() {
  if (!meal_name_validation.value) return false

  for (const ingredient of meal_validation.value) {
    const result = checkValidationArr(ingredient)
    if (!result) return result
  }

  return true
}

async function addIngredientToMeal(ingredient: Ingredient) {
  if (
    ingredient.ingredient_id &&
    !checkIfIngredientIsAlreadyAdded(ingredient.ingredient_id, 'ingredient_id')
  ) {
    ingredientsData.value.push(ingredient)

    let _ingredient_validation = deepClone(ingredient_validation)

    _ingredient_validation.amount = true
    _ingredient_validation.name = true

    meal_validation.value.push(_ingredient_validation)

    alertSuccess()
    await _alert(`Successfully added ${ingredient.name}`)
  } else {
    alertDanger()
    await _alert('You can not add the same ingredient. Instead change the amount')
  }
}

function checkIfIngredientIsAlreadyAdded(id_to_compare: number, key: string) {
  for (const ingredient of ingredientsData.value) {
    if (ingredient[key] == id_to_compare) {
      return true
    }
  }

  return false
}

async function addAPIProductToMeal(product: any) {
  if (!checkIfIngredientIsAlreadyAdded(product['id'], 'api_product_id')) {
    ingredientsData.value.push({
      api_product_id: product['id'],
      amount: `${product['weight']} ${product['weight_unit']}`,
      calories: product['nutrition'][0]['amount'],
      carbohydrates: product['nutrition'][2]['amount'],
      fat: product['nutrition'][1]['amount'],
      sugar: product['nutrition'][4]['amount'],
      name: product['name'],
      protein: product['nutrition'][3]['amount']
    })

    alertSuccess()
    await _alert(`Successfully added ${product['name']}`)
  } else {
    alertDanger()
    await _alert('You can not add the same ingredient from kassal app')
  }
}

async function load_products_from_api_search() {
  if (api_search.value.length > 2) {
    try {
      const url = `https://kassal.app/api/v1/products?search=${api_search.value}`
      const headers = { Authorization: `Bearer ${import.meta.env.VITE_KASSAL_API_KEY}` }

      const _response = await fetch(url, { headers: headers })

      const data = await _response.json()

      // Filtering out the products which does not have nutrition information
      for (let product of data['data']) {
        if (product['nutrition'].length > 0) {
          const arr = []
          for (let nutrition of product['nutrition']) {
            if (
              ['Protein', 'Sukkerarter', 'Karbohydrater', 'Fett', 'Kalorier'].includes(
                nutrition['display_name']
              ) &&
              nutrition['amount'] >= 0
            ) {
              arr.push(nutrition)
            }
          }
          product['nutrition'] = arr
        }
      }

      api_search_data.value = data
    } catch (error) {
      console.log(error)
      alert(`Network error: ${error}`)
    }
  }
}

async function addEmptyIngredient() {
  ingredientsData.value.push({
    name: '',
    amount: 0,
    protein: 0,
    calories: 0,
    carbohydrates: 0,
    fat: 0,
    sugar: 0
  })
  meal_validation.value.push(deepClone(ingredient_validation))

  alertSuccess()
  await _alert(`Successfully added an empty ingredient`)
}

async function removeEntry(index: number) {
  const ingredient_name =
    ingredientsData.value[index].name == ''
      ? 'the empty ingredient'
      : ingredientsData.value[index].name

  ingredientsData.value.splice(index, 1)
  meal_validation.value.splice(index, 1)

  alertSuccess()
  await _alert(`Successfully removed ${ingredient_name}`)
}

async function handleDeleteIngredientFromMeal(
  ingredient_id: number | undefined,
  meal_id: number,
  arr_index: number
) {
  if (ingredient_id) {
    const response = await deleteEntity(`/meal/${ingredient_id}/${meal_id}`)

    if (response && response.ok) {
      removeEntry(arr_index)
    }
  }
}

function handleCreateIngredientEvent() {
  hideAlert()
  changeValidationForNameAndAmount(false)
}

async function triggerMealEvent() {
  if (check_meal_validation()) {
    const json = getFormDataInJSONFormat(`${props.formulate_type}_meal_form`)
    const response = await fetchResource(http_method.value, json, url.value, 'token', modal_id)

    if (response) {
      // update list of meals

      if (response.ok) {
        await getMeals()
      }

      if (response.status == 401 || response.ok) {
        hideModal(modal_id)
      }
    }
  } else {
    alertDanger()
    await _alert(
      "Fill out the required fields: 'Meal Name'. 'Name' and 'Amount' for each ingredient is required. Nutrient values may be zero."
    )
  }
}

const api_search = ref<string>('')
</script>

<template>
  <FormulateIngredient formulate_type="create" />

  <div class="modal modal-xl fade Modal" tabindex="-1" :id="modal_id">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">{{ _formulate_type }} a meal</h3>
          <button class="btn btn-lg ms-auto" @click="hideAlert()" data-bs-dismiss="modal">
            <font-awesome-icon :icon="['fas', 'x']" />
          </button>
        </div>

        <div class="modal-body">
          <form :id="`${formulate_type}_meal_form`" @submit.prevent>
            <AlertBox />

            <label for="meal_name"> Meal name: </label>

            <input style="width: 80%" @input="
              meal_name_validation = ValidateText(
                $event,
                meal_name_message_validation,
                'MealName',
                'form-control form-control-md'
              )
              " class="form-control form-control-md" ref="meal_name_input" name="meal_name" type="text"
              v-model="meal_name" />

            <div ref="meal_name_message_validation" class="ml-2 invalid-feedback"></div>

            <div class="mt-2 mb-1">
              <h5>Ingredients</h5>
            </div>
            <h6 class="ml-3" v-if="ingredientsData.length == 0">Your meal has zero ingredients</h6>
            <div class="column">
              <div class="row">
                <template v-if="ingredientsData.length > 0">
                  <div class="column form-group ml-4" v-for="(ingredient, index) in ingredientsData" :key="index"
                    style="max-width: 200px">
                    <input :name="index + '-ingredient_id'" type="text" :value="ingredient.ingredient_id"
                      style="display: none" />

                    <IngredientInputModule :ingredient="ingredient" food_type="meal" :index="index"
                      :random="randomNumber" />

                    <div class="mt-2 btn-group-md btn-group d-flex">
                      <button v-if="ingredient.meal_id" type="button" class="btn-outline-danger btn btn-md" @click="
                        handleDeleteIngredientFromMeal(
                          ingredient.ingredient_id,
                          ingredient.meal_id,
                          index
                        )
                        ">
                        Remove <font-awesome-icon :icon="['fas', 'trash']" />
                      </button>
                      <button v-else type="button" class="btn-outline-danger btn btn-md" @click="removeEntry(index)">
                        Remove <font-awesome-icon :icon="['fas', 'trash']" />
                      </button>
                    </div>
                  </div>
                </template>
              </div>
              <div class="ml-3 mt-3">
                <h5>Select and click the ingredient you want to add</h5>
                <div class="wrap">
                  <div v-for="ingredient in ingredients" :key="ingredient.ingredient_id">
                    <button type="button" @click="addIngredientToMeal(ingredient)" class="btn btn-secondary btn-md m-2">
                      <h6>{{ ingredient['name'] }}</h6>
                    </button>
                  </div>
                </div>
                <div class="ml-3" v-if="ingredients && ingredients.length == 0">
                  <h6>You don't have any ingredients</h6>
                  <button type="button" class="btn-success btn btn-sm" data-bs-toggle="modal"
                    data-bs-target="#create_ingredient_modal" @click="handleCreateIngredientEvent()">
                    <h6>Create ingredient</h6>
                  </button>
                </div>
              </div>
              <section class="m-2">
                <h4>Find ingredients with Kassal.app API</h4>

                <form @submit.prevent>
                  <div class="input-group m-1">
                    <input class="form-control" v-model="api_search" placeholder="Search for ingredient" type="text" />
                    <button type="submit" class="btn btn-primary" @click="load_products_from_api_search()">
                      Find product
                    </button>
                  </div>
                </form>

                <div v-if="api_search_data">
                  <div class="wrap justify-content-center mb-5">
                    <div v-for="(product, index) in api_search_data.data" :key="index" class="rounded m-4 product">
                      <div class="d-flex flex-column align-items-center">
                        <ul class="list-group">
                          <li class="list-group-item list-group-item-info">
                            {{ product['name'] }}
                          </li>
                          <li v-for="nutrient in product['nutrition']" class="list-group-item"
                            :key="nutrient.display_name">
                            {{ nutrient['display_name'] }}: {{ nutrient['amount'] }}
                            {{ nutrient['unit'] }}
                          </li>
                          <li class="list-group-item">Price: {{ product['current_price'] }} kr</li>
                        </ul>

                        <img style="width: 100%; height: 200px; object-fit: contain" class="mt-1 mb-2 rounded"
                          :src="product['image']" :alt="product['name']" />

                        <button type="button" class="btn btn-info btn-md" @click="addAPIProductToMeal(product)">
                          Add {{ product['name'] }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <h5 class="ml-4" v-if="
                  api_search_data && api_search_data.data.length == 0 && api_search.length > 2
                ">
                  Please click enter or button *Find product*, if already done; sorry did not find
                  any products with your search: {{ api_search }}
                </h5>
                <h5 class="ml-4" v-if="!api_search_data && api_search.length != 0 && api_search.length < 3">
                  Your search: {{ api_search }} is too short. Minium 3 letters
                </h5>
              </section>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary btn-lg ml-1" @click="addEmptyIngredient()">
            <font-awesome-icon :icon="['fas', 'plus']" /> Empty Ingredient
          </button>
          <div v-if="fetchingResource">
            <RequestLoader />
          </div>
          <button :disabled="fetchingResource" type="button" @click="triggerMealEvent()"
            class="btn btn-success btn-lg ml-1">
            {{ _formulate_type }} Meal
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product {
  background-color: rgb(39, 38, 38);
}

button {
  z-index: 0;
}
</style>
