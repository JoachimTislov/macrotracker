import { ref, watch } from 'vue'

export const user_id = ref<string | null>(localStorage.getItem('user_id'))
watch(user_id, (newValue) => {
  if (newValue) {
    localStorage.setItem('user_id', newValue.toString())
  } else {
    localStorage.removeItem('user_id')
  }
})

export const token = ref<string | null>(localStorage.getItem('token'))
watch(token, (newValue) => {
  if (newValue) {
    localStorage.setItem('token', newValue)
  } else {
    localStorage.removeItem('token')
  }
})

const storedUsername = localStorage.getItem('username')
export const username = ref<string>(storedUsername ? storedUsername : '')
watch(username, (newValue) => {
  if (newValue) {
    localStorage.setItem('username', newValue)
  } else {
    localStorage.removeItem('username')
  }
})
