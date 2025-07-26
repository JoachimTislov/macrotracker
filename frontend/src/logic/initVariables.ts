import { reactive, ref, type Ref } from 'vue'
import {
  type Calender_data,
  type Ingredients,
  type Meal_with_ingredients,
  type Meals_for_time_of_day,
  type Stats_for_dates,
  type UserInfo,
  type Validation_array,
  type validation_Object
} from './types'
import { getData } from './Ajax/ajax'
import user_icon from '@/assets/icons/user-icon.png'
import { getTodaysDate_FriendlyFormatDateInput } from './dateSystem'
import { _alert, alertSuccess } from './alertFunctions'
import deepClone from './deepClone'

export const fetchingResource = ref<boolean>(false)

export const warningMessage = `The initial request to the server, such as login or registration, 
might take a while because the service hosted on Render.com shuts down when theres been no recent activity.`

export const ingredient_validation = {
  name: false,
  amount: false,
  protein: true,
  calories: true,
  carbohydrates: true,
  fat: true,
  sugar: true
}

export const createOrEdit_ingredient_validation_arr: Validation_array = reactive(
  deepClone(ingredient_validation)
)

export const meal_name_validation = ref<boolean>(false)
export const meal_validation = ref<validation_Object[]>([])

export const showAlert = ref<boolean>(false)
export const alertMessage = ref<string>('')
export const alertClassName = ref<string>('')

export const password = ref<string>('')

export const login_validation = reactive({
  Username: localStorage.getItem('username') ? true : false,
  Password: false
})

export const change_password_validation: Validation_array = reactive({
  old_password: false,
  new_password: false,
  new_confirm_password: false
})

export const user_validation_arr: { [key: string]: boolean } = reactive({
  username: false,
  password: false,
  confirm_password: false,
  gender: false,
  activityLvl: false,
  email: false,
  weight: false,
  height: false,
  age: false,
  name: false
})

export const validation_messages: {
  [key: string]: {
    [key: string]: Ref<HTMLElement | null>
  }
} = {
  login: {
    username: ref<HTMLElement | null>(null),
    password: ref<HTMLElement | null>(null)
  },
  register: {
    gender: ref<HTMLElement | null>(null),
    activity_lvl: ref<HTMLElement | null>(null)
  }
}

export function initAlertElements() {
  for (const category of Object.keys(validation_messages)) {
    for (const element of Object.keys(validation_messages[category])) {
      validation_messages[category][element].value?.focus()
    }
  }
}

//////////////// Data init //////////////////////

export const zero_meals_for_time_period = ref<boolean>(false)

export const selected_start_date = ref<string>(getTodaysDate_FriendlyFormatDateInput())
export const selected_end_date = ref<string>(getTodaysDate_FriendlyFormatDateInput())

export const selectedDate = ref<string>(getTodaysDate_FriendlyFormatDateInput())

export const meals_for_time_of_day = ref<Meals_for_time_of_day | {}>({})
export const dates_within_selected_period = ref<string[]>([])

// Used in statistics
export const StatsToShow = ref<boolean>(false)

export const labels = ['Calories', 'Protein', 'Carbohydrates', 'Fat', 'Sugar']
export const overall_stats = reactive({
  total: [0, 0, 0, 0, 0],
  average: [0, 0, 0, 0, 0]
})

export const stats_for_dates: Stats_for_dates = reactive({})

export const eaten_nutrient_progression: { [key: string]: number[] } = reactive({
  calories: [0],
  protein: [0],
  carbohydrates: [0],
  fat: [0],
  sugar: [0]
})

////////////////////////////////////////

// Personal schedule, might store this in the database
export const schedule: { [key: string]: { Start: number; End: number } } = {
  Breakfast: { Start: 6, End: 11 },
  Lunch: { Start: 12, End: 15 },
  Dinner: { Start: 16, End: 20 },
  Supper: { Start: 21, End: 24 },
  Night: { Start: 0, End: 5 }
}

export const recommended_nutrient_data: number[] = reactive([])
export const userInfo = ref<UserInfo | undefined>(undefined)

export const calender_data = ref<Calender_data>({})
export const meals = ref<Meal_with_ingredients[] | undefined>(undefined)
export const ingredients = ref<Ingredients | undefined>(undefined)

/////////////////////////////////////////////////

//////////////////////// Image find picture ////////////////////////////////////////

// https://www.zhenghao.io/posts/verify-image-url
function canFindImage(url: string) {
  const img = new Image()
  img.src = url
  return new Promise((resolve) => {
    img.onload = () => resolve(true)
    img.onerror = () => resolve(false)
  })
}

export const _file = ref<File | null>(null)
export const profilePictureUrl = ref<string>(user_icon)
export const uploadedPicture = ref<boolean>(false)

export async function initPicture() {
  const storedImageInfo = localStorage.getItem('imageUrl')
  const imageInfo: { url: string; user_id: string } | null = storedImageInfo
    ? JSON.parse(storedImageInfo)
    : null

  const user_id = localStorage.getItem('user_id')

  if (imageInfo && imageInfo.user_id === user_id && (await canFindImage(imageInfo.url))) {
    profilePictureUrl.value = imageInfo.url
    uploadedPicture.value = true
  } else {
    const response = await getData(`/user_picture/${user_id}`)

    if (response && response.ok) {
      if (response.headers.get('Content-Type')?.split('/')[0] == 'image') {
        const blob = await response.blob()
        const userPictureURL = URL.createObjectURL(blob)

        const imageInfo = JSON.stringify({ url: userPictureURL, user_id: user_id })
        localStorage.setItem('imageUrl', imageInfo)
        profilePictureUrl.value = userPictureURL
        uploadedPicture.value = true
      } else {
        const result = await response.json()
        alertSuccess()
        await _alert(result.message)
      }
    }
  }
}

////////////////////////////////////////////////////////////////
