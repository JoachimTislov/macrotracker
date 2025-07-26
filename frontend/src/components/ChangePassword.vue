<script setup lang="ts">
import { checkValidationArr } from '@/logic/checkLogic/checkValidationArr'
import AlertBox from './Modules/AlertBox.vue'
import PasswordInput from './Modules/PasswordInput.vue'
import { change_password_validation } from '@/logic/initVariables'
import { _alert, alertDanger, hideAlert } from '@/logic/alertFunctions'
import { fetchResource } from '@/logic/Ajax/ajax'
import { getFormDataInJSONFormat } from '@/logic/Ajax/get/getFormDataInJSONFormat'

const password_inputs = [
  { name: 'old_password', label: 'Old' },
  { name: 'new_password', label: 'New' },
  { name: 'new_confirm_password', label: 'Repeat New' }
]

const modal_id = 'change_password_modal'

async function changePassword() {
  if (checkValidationArr(change_password_validation)) {
    try {
      const json = getFormDataInJSONFormat('passwords')
      const user_id = localStorage.getItem('user_id')

      await fetchResource('PUT', json, `/password/${user_id}`, 'token', modal_id)
    } catch (error) {
      console.log(error)
      alert(`Network error: ${error}`)
    }
  } else {
    alertDanger()
    await _alert('Fill out the password fields correctly')
  }
}
</script>

<template>
  <div class="modal modal-sm fade Modal" :id="modal_id">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title m-2">Change Password</h4>
          <button class="btn btn-lg ms-auto" @click="hideAlert()" data-bs-dismiss="modal">
            <font-awesome-icon :icon="['fas', 'x']" />
          </button>
        </div>

        <div class="modal-body">
          <AlertBox />

          <form id="passwords" @submit.prevent>
            <template v-for="password_input in password_inputs" :key="password_input">
              <PasswordInput :password_details="password_input" />
            </template>
          </form>
        </div>
        <div class="modal-footer">
          <button type="submit" @click="changePassword()" class="btn btn-success">
            Change Password
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
