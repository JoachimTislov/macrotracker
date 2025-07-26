import { login } from './Ajax/login'
import { _alert, alertSecondary } from './alertFunctions'
import { fetchingResource, login_validation, password } from './initVariables'
import { username } from './variables'

export async function initiateExampleAccount() {
  if (fetchingResource.value) {
    await _alert('Already login into example account...')
  } else {
    alertSecondary()
    await _alert('Login into the example account, this might take some time')

    username.value = 'Peddi'
    login_validation.Username = true

    password.value = 'peder@123'
    login_validation.Password = true

    await login()
  }
}
