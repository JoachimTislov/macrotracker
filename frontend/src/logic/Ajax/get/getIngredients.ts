import { ingredients } from '../../initVariables'
import type { Ingredients } from '../../types'
import { getData } from '../ajax'

export async function getIngredients() {
  const user_id = localStorage.getItem('user_id')
  const ingredients_response = await getData(`/personal_ingredients/${user_id}`)
  ingredients.value = ingredients_response
    ? ((await ingredients_response.json()) as Ingredients)
    : undefined
}
