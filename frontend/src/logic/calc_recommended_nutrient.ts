import { recommended_nutrient_data, userInfo } from './initVariables'

//Source: https://mohap.gov.ae/en/more/awareness-center/calories-calculation#:~:text=If%20you%20are%20sedentary%20(little,Calorie%2DCalculation%20%3D%20BMR%20x%201.55
//https://www.k-state.edu/paccats/Contents/Nutrition/PDF/Needs.pdf
export function calc_recommended_nutrient() {
  if (userInfo.value) {
    const weight = parseInt(userInfo.value.Weight)
    const gender = userInfo.value.Gender

    const calories = calculate_recommended_calories(
      parseInt(userInfo.value.Weight),
      parseInt(userInfo.value.Height),
      gender,
      parseInt(userInfo.value.Age),
      userInfo.value['Activity lvl']
    )
    const protein = Math.round(weight * 0.9)
    const carbohydrates = Math.round((calories * 0.55) / 4)
    const fat = Math.round((calories * 0.3) / 9)

    const sugar = gender == 'Male' ? 36 : 25

    const arr = [calories, protein, carbohydrates, fat, sugar]

    for (let i = 0; i < arr.length; i++) {
      recommended_nutrient_data[i] = arr[i]
    }
  }
}

function calculate_recommended_calories(
  weight: number,
  height: number,
  gender: string,
  age: number,
  activity_lvl: string
) {
  let BMR = 10 * weight + 6.25 * height - 5 * age

  if (gender == 'Male') {
    BMR += 5
  } else {
    BMR -= 161
  }

  const caloriesMapping: { [key: string]: number } = {
    Sedentary: Math.round(BMR * 1.2),
    'Lightly Active': Math.round(BMR * 1.375),
    'Moderately Active': Math.round(BMR * 1.55),
    'Very Active': Math.round(BMR * 1.725),
    'Super Active': Math.round(BMR * 1.9)
  }

  return caloriesMapping[activity_lvl]
}
