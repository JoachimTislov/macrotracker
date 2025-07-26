import { meals } from '../../initVariables'
import type { Meal_with_ingredients } from '../../types'
import { getData } from '../ajax'

export async function getMeals() {
  const user_id = localStorage.getItem('user_id')
  const meals_response = await getData(`/personal_meals/${user_id}`)
  meals.value = meals_response
    ? ((await meals_response.json()) as Meal_with_ingredients[])
    : undefined
}
