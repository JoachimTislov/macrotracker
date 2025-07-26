import { alertClassName, alertMessage, showAlert } from './initVariables'

export const delay = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms))

export function hideAlert() {
  showAlert.value = false
}

export function revealAlert() {
  showAlert.value = true
}

export function alertDanger() {
  alertClassName.value = 'alert-danger'
}

export function alertSuccess() {
  alertClassName.value = 'alert-success'
}

export function alertSecondary() {
  alertClassName.value = 'alert-secondary'
}

export async function _alert(message: string) {
  revealAlert()
  alertMessage.value = message

  const oldClassName = alertClassName.value
  alertClassName.value = oldClassName + ' smoothIn'
  await delay(500)
  alertClassName.value = oldClassName
}
