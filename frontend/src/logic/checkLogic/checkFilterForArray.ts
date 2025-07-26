import { filterArrayByName, sortArray } from '../sorting'
import type { Ingredients } from '../types'

export function checkFilterForArray<
  Type extends { [key: string]: number | string | Ingredients | undefined }
>(arr: Type[] | undefined, search_value: string, sort_value: string) {
  if (search_value.length > 0) {
    arr = filterArrayByName(arr, search_value)
  }

  if (sort_value != 'Sort By') {
    arr = sortArray(arr, sort_value)
  }

  return arr
}
