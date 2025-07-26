import { profilePictureUrl, uploadedPicture } from '../initVariables'
import { deleteEntity } from './ajax'
import user_icon from '@/assets/icons/user-icon.png'

export async function deleteProfilePicture() {
  try {
    const response = await deleteEntity('/profile_picture')

    if (response && response.ok) {
      profilePictureUrl.value = user_icon
      localStorage.removeItem('imageUrl')

      uploadedPicture.value = false
    }
  } catch (error) {
    console.error('Error deleting profile picture:', error)
  }
}
