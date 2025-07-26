import { _alert, alertDanger } from '../alertFunctions'
import { initPicture, uploadedPicture, _file } from '../initVariables'
import { fetchResource } from './ajax'
import { deleteProfilePicture } from './deleteProfilePicture'

export async function uploadProfilePicture(file: Blob | null) {
  if (!file) {
    alertDanger()
    await _alert('No file selected')
  } else {
    try {
      // Delete old picture
      if (uploadedPicture.value) await deleteProfilePicture()

      const form_data = new FormData()
      form_data.append('file', file)

      const response = await fetchResource('POST', form_data, '/profile_picture', 'token')

      if (response && response.ok) {
        initPicture()

        const fileInput = document.getElementById('pictureInput') as HTMLInputElement
        fileInput.value = ''

        _file.value = null
        uploadedPicture.value = true
      }
    } catch (error) {
      console.error('Error when uploading profile picture: ', error)
    }
  }
}
