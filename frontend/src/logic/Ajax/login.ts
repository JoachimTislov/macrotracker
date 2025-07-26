import router from '@/router'
import { _alert, alertDanger, alertSuccess } from '../alertFunctions'
import { fetchingResource, login_validation, password } from '../initVariables'
import { token, user_id, username } from '../variables'
import { fetchResource } from './ajax'

export async function login() {
  if (login_validation.Password && login_validation.Username && !fetchingResource.value) {
    try {
      const json = JSON.stringify({
        username: username.value,
        password: password.value
      })

      const response = await fetchResource('POST', json, '/login', 'api_key')

      if (response) {
        const result: {
          message: string
          token: string
          user_id: string
          username: string
        } = await response.json()

        // TODO: Probably rework this underneath
        // Should actually rework everything ...

        if (response.ok) {
          token.value = result.token
          user_id.value = result.user_id
          username.value = result.username

          router.push({ name: 'macroHome' })
          alertSuccess()

          if (user_id.value == '1') {
            await _alert('You have logged into the example account successfully')
          } else {
            await _alert('You have logged into your account successfully')
          }
        } else {
          alertDanger()
          await _alert(result.message)
        }
      }
    } catch (error) {
      alert('Error logging in: ' + error)
    }
  } else {
    alertDanger()
    if (fetchingResource.value) {
      await _alert('Already login in...')
    } else {
      await _alert(
        `Fill out the ${!login_validation.Username ? 'Username' : 'Password'} field correctly!`
      )
    }
  }
}
