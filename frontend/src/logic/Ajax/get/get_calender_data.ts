import { calender_data } from '../../initVariables'
import { structureCalenderData } from '../../structure_calender_data'
import type { Calender_data } from '../../types'
import { getData } from '../ajax'

export async function get_calender_data() {
  const user_id = localStorage.getItem('user_id')
  const url = `/calender_data/${user_id}`
  const response = await getData(url)
  const calender_data_response: Calender_data = await response?.json()

  calender_data.value = calender_data_response

  structureCalenderData()
}
