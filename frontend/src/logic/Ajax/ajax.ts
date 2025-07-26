import { token, user_id, username } from '../variables'
import { fetchingResource, password } from '../initVariables'
import { _alert, alertDanger, alertSecondary, alertSuccess } from '../alertFunctions'
import router from '@/router'
import { hideModal } from '../hideModal'

function load() {
  fetchingResource.value = true
}

function unLoad() {
  fetchingResource.value = false
}

export function removeLocalData() {
  token.value = null
  user_id.value = null
  username.value = ''
  password.value = ''
}

function checkIfUserIsUnAuthorized(response: Response, modal_id?: string) {
  if (response.status == 401) {
    if (modal_id) {
      hideModal(modal_id)
    }
    forceFullyLogTheUserOut()
  } else {
    return response
  }
}

function handleNetworkError() {
  alertDanger()
  _alert('Sorry, but we are having issues with the server hosted on render.com')
}

function forceFullyLogTheUserOut() {
  removeLocalData()
  alertSecondary()
  _alert('Your session has expired')
  router.push({ name: 'macroLogin' })
}

export async function getData(url: string) {
  if (!token.value) {
    forceFullyLogTheUserOut()
  } else {
    try {
      load()

      const endpoint = `${import.meta.env.VITE_MACROTRACKER_API_WEB_URL}${url}`
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          Authorization: user_id.value == '1' ? user_id.value : token.value
        }
      })

      unLoad()

      return checkIfUserIsUnAuthorized(response)
    } catch (error) {
      unLoad()
      handleNetworkError()
    }
  }
}

export async function deleteEntity(
  url: string,
  func?: () => Promise<void>,
  calenderFunc?: (identifier?: string) => void
) {
  if (!token.value) {
    forceFullyLogTheUserOut()
  } else {
    if (confirm('Are you sure?')) {
      try {
        load()

        const endpoint = `${import.meta.env.VITE_MACROTRACKER_API_WEB_URL}${url}`
        const response = await fetch(endpoint, {
          method: 'DELETE',
          headers: {
            // Example account by pass
            Authorization: user_id.value == '1' ? user_id.value : token.value
          }
        })

        if (response.ok) {
          if (func) {
            await func()
          }

          if (calenderFunc) {
            calenderFunc()
          }
        }

        if (response.ok) {
          alertSuccess()
        } else {
          alertDanger()
        }

        const message = (await response.json()).message
        _alert(message)

        unLoad()

        return checkIfUserIsUnAuthorized(response)
      } catch (error) {
        unLoad()
        handleNetworkError()
      }
    }
  }
}

export async function fetchResource(
  method: string,
  data: string | FormData,
  url: string,
  typeOfAuth: string | undefined,
  modal_id?: string
): Promise<Response | undefined> {
  const api_key: string = import.meta.env.VITE_MACROTRACKER_API_KEY
  let auth = typeOfAuth == 'api_key' ? api_key : token.value
  if (!auth) {
    forceFullyLogTheUserOut()
  } else {
    const endpoint = `${import.meta.env.VITE_MACROTRACKER_API_WEB_URL}${url}`

    // Example account by pass
    auth = user_id.value == '1' ? user_id.value : auth

    const fetchBody = {
      method: method,
      headers: {
        Authorization: auth,
        ...(!(data instanceof FormData) && { 'Content-Type': 'application/json' })
      },
      body: data
    }

    try {
      load()

      const response = await fetch(endpoint, fetchBody)

      if (response.headers.get('Content-Type') == 'application/json' && url !== '/login') {
        const message = (await response.json()).message

        if (response.ok) {
          if (modal_id) {
            hideModal(modal_id)
          }
          alertSuccess()
        } else {
          alertDanger()
        }

        _alert(message)
      }

      unLoad()

      return checkIfUserIsUnAuthorized(response, modal_id)
    } catch (error) {
      unLoad()
      handleNetworkError()
    }
  }
}
