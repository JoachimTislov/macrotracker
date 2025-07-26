import type { Ref } from 'vue'

export type Calender_data = {
  [key: string]: calender_data_entry[]
}

export type calender_data_entry = {
  calender_id: number
  date: string
  meal: Meal
  time_of_day: string
}

export type macros_statistics = {
  series: number[]
  options: {
    [key: string]: string[]
  }
}

export type Stats_for_dates = {
  [key: string]: {
    total: number[]
    average: number[]
    meals: {
      [key: string]: {
        data: number[]
      }
    }
  }
}

export type Meal = {
  [key: string]: string | number
  name: string
  calories: number
  carbohydrates: number
  fat: number
  meal_id: number
  protein: number
  sugar: number
  user_id: number
}

export type Meal_with_ingredients = Meal & {
  [key: string]: string | number | Ingredients

  ingredients: Ingredients
}

type MealPeriods = {
  [key: string]: calender_data_entry[]
  Breakfast: calender_data_entry[]
  Lunch: calender_data_entry[]
  Dinner: calender_data_entry[]
  Supper: calender_data_entry[]
  Night: calender_data_entry[]
}

export type Meals_for_time_of_day = {
  [date: string]: {
    meal_periods: MealPeriods
    zero_meals_to_show: boolean
  }
}

export type Ingredients = Ingredient[]

export type Ingredient = {
  [key: string]: string | number | undefined
  ingredient_id?: number
  api_product_id?: number
  meal_id?: number
  name: string
  amount: number | string
  protein: number
  calories: number
  carbohydrates: number
  fat: number
  sugar: number
}

export type Api_search_data = {
  data: api_entry[]
  meta: {
    current_page: number
    from: number
    path: string
    per_page: number
    to: number
  }
  links: {
    first: string
    last?: string
    prev?: string
    next: string
  }
}

export type api_entry = {
  id: number
  name: string
  brand: string
  vendor: string
  ean: string
  updated_at: string
  url: string
  weight: number
  weight_unit: string
  store: {
    code: string
    logo: string
    name: string
    url: string
  }
  price_history: {
    price: number
    date: string
  }[]
  nutrition: {
    code: string
    display_name: string
    amount: number
    unit: string
  }[]
  labels: {
    name: string
    display_name: string
    description: string
  }[]
  ingredients: string
  image: string
  description: string
  current_unit_price: string
  current_price: string
  created_at: string
  category: {
    id: number
    depth: number
    name: string
  }
  allergens: {
    code: string
    display_name: string
    contains: string
  }
}

export type validation_Object = { [key: string]: boolean }

export type IngredientModal = {
  [key: string]: {
    formulate_type: string
    ingredient?: Ingredient | undefined
  }
}

export type mealModal = {
  [key: string]: {
    formulate_type: string
    meal?: Meal_with_ingredients | undefined
  }
}

export type Form_configuration = IngredientInfo[]

export type IngredientInfo = {
  identifier: string
  validation_type: string
  inputType: string
  value?: string | number
  class: string
  unit?: string
  random?: number
}

export type Validation_array = { [key: string]: boolean }

export type ValidationRefs = { [key: string]: Ref<HTMLElement | null> }

export type UserInfo = { [key: string]: string }

export type User_input_field = {
  inputType: string
  placeholder: string
  validate_type: string
  identifier: string
  class: string
  attachment?: string
  type?: string
  value?: string
}
