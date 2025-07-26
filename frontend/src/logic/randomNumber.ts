import { ref } from 'vue'

export const randomNumber = ref<number>(getRandomInt(1000))

function getRandomInt(max: number) {
  return Math.random() * max
}

export function generateRandomNumber() {
  randomNumber.value = getRandomInt(1000)
}
