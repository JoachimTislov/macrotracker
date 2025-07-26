export function checkValidationArr(validation_arr: { [key: string]: boolean }) {
  for (const key of Object.keys(validation_arr)) {
    if (validation_arr[key] === false) {
      return false
    }
  }
  return true
}
