export function splitArrayWithRespectToSortedArray<T>(arr: T[] | undefined): T[][] {
  if (!arr || arr.length == 0) return [[], []]

  const arr_1: T[] = []
  const arr_2: T[] = []

  for (let i = 0; i < arr.length; i++) {
    if (i % 2 == 0) {
      arr_1.push(arr[i])
    } else {
      arr_2.push(arr[i])
    }
  }

  return [arr_1, arr_2]
}
