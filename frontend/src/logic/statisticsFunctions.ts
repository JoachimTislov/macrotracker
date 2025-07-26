import {
  eaten_nutrient_progression,
  labels,
  recommended_nutrient_data,
  overall_stats,
  StatsToShow,
  calender_data,
  dates_within_selected_period,
  stats_for_dates
} from './initVariables'
import { getDate } from './dateSystem'

function resetOverallStats() {
  const arr = [overall_stats.average, overall_stats.total]

  for (const stats of arr) {
    for (let i = 0; i < stats.length; i++) {
      stats[i] = 0
    }
  }
}

export function calcNutrientStatsForGivenPeriod() {
  resetOverallStats()
  // Adding all of the nutrients for the given week

  if (calender_data.value) {
    if (!calender_data.value[dates_within_selected_period.value[0]]) {
      StatsToShow.value = false
      return
    }

    let meal_amount = 0
    for (const date of dates_within_selected_period.value) {
      stats_for_dates[date] = {
        total: [0, 0, 0, 0, 0],
        average: [0, 0, 0, 0, 0],
        meals: {}
      }
      if (calender_data.value[date] && calender_data.value[date].length > 0) {
        meal_amount += calender_data.value[date].length
        for (const calender_entry of calender_data.value[date]) {
          const meal = calender_entry.meal
          if (!stats_for_dates[date].meals[meal.name]) {
            stats_for_dates[date].meals[meal.name] = {
              data: [meal.calories, meal.protein, meal.carbohydrates, meal.fat, meal.sugar]
            }
          }

          for (let i = 0; i < labels.length; i++) {
            const arr = [stats_for_dates[date], overall_stats]
            for (let j = 0; j < arr.length; j++) {
              arr[j].total[i] += calender_entry.meal[labels[i].toLocaleLowerCase()] as number
            }

            if (overall_stats.total[i] > 0) {
              StatsToShow.value = true
            }
          }
        }

        for (let i = 0; i < labels.length; i++) {
          if (stats_for_dates[date].total[i] != 0) {
            stats_for_dates[date].average[i] = Math.round(
              stats_for_dates[date].total[i] / Object.keys(stats_for_dates[date].meals).length
            )
          }
        }
      }
    }

    for (let i = 0; i < labels.length; i++) {
      if (overall_stats.total[i] != 0) {
        overall_stats.average[i] = Math.round(overall_stats.total[i] / meal_amount)
      }
    }
  }
}

export function setupNutrientProgressChartsData() {
  if (calender_data.value) {
    const mealsEatenToday = calender_data.value[getDate()]

    for (const key of Object.keys(eaten_nutrient_progression)) {
      eaten_nutrient_progression[key] = [0]
    }

    if (mealsEatenToday) {
      for (const entry of mealsEatenToday) {
        eaten_nutrient_progression.calories[0] += entry.meal.calories
        eaten_nutrient_progression.protein[0] += entry.meal.protein
        eaten_nutrient_progression.carbohydrates[0] += entry.meal.carbohydrates
        eaten_nutrient_progression.fat[0] += entry.meal.fat
        eaten_nutrient_progression.sugar[0] += entry.meal.sugar
      }

      Object.entries(eaten_nutrient_progression).forEach(([, value], index) => {
        if (value && recommended_nutrient_data[index]) {
          value[0] = Math.round((value[0] / recommended_nutrient_data[index]) * 100)
        }
      })
    }
  }
}
