export function check_if_number_is_less_than_10(int: number) {
  if (int < 10) {
    return '0' + int
  } else {
    return int
  }
}
