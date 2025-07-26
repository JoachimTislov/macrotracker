import { Modal } from 'bootstrap'

export function hideModal(id: string) {
  const modal = document.getElementById(id) as HTMLElement
  Modal.getInstance(modal)?.hide()
}
