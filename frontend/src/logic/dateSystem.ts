import { check_if_number_is_less_than_10 } from './checkLogic/check_if_number_is_less_than_10'

// Object date friendly
const days_in_a_week = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday'
]

const determineDateObject = (date?: string) => {
  return date ? new Date(date) : new Date()
}

export function getDayForDate(date: string) {
  const dateObject = new Date(convertNODateToAmerican(date))
  return days_in_a_week[dateObject.getDay()]
}

export function getDate(date?: string) {
  const dateObject = determineDateObject(date)
  return `${check_if_number_is_less_than_10(dateObject.getDate())}-${check_if_number_is_less_than_10(dateObject.getMonth() + 1)}-${dateObject.getFullYear()}`
}

export function getDate_AmericanFormat(date?: string) {
  const dateObject = determineDateObject(date)
  return `${check_if_number_is_less_than_10(dateObject.getMonth() + 1)}-${check_if_number_is_less_than_10(dateObject.getDate())}-${dateObject.getFullYear()}`
}

export function getTodaysDate_FriendlyFormatDateInput(date?: string) {
  // Have to edit it to format yyyy-mm-dd
  const dateObject = determineDateObject(date)
  return `${dateObject.getFullYear()}-${check_if_number_is_less_than_10(dateObject.getMonth() + 1)}-${check_if_number_is_less_than_10(dateObject.getDate())}`
}

function convertNODateToAmerican(date: string): string {
  const [day, month, year] = date.split('-')
  return `${month}-${day}-${year}`
}

export function reverseInputDateFormat(date: string): string {
  const [year, month, day] = date.split('-')
  return `${day}-${month}-${year}`
}

export function convertToInputDateFormat(date: string): string {
  const [day, month, year] = date.split('-')
  return `${year}-${month}-${day}`
}
