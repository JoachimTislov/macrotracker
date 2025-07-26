<script setup lang="ts">
import { fetchResource } from '@/logic/Ajax/ajax'
import { getFormDataInJSONFormat } from '@/logic/Ajax/get/getFormDataInJSONFormat'
import {
  fetchingResource,
  login_validation,
  password,
  user_validation_arr,
  warningMessage
} from '@/logic/initVariables'
import { checkValidationArr } from '@/logic/checkLogic/checkValidationArr'
import AlertBox from './Modules/AlertBox.vue'
import { username } from '@/logic/variables'
import { _alert, alertDanger, alertSuccess } from '@/logic/alertFunctions'
import RegisterModule from './Modules/RegisterModule.vue'
import RequestLoader from './RequestLoader.vue'
import router from '@/router'
import WarningModule from './Modules/WarningModule.vue'

async function register() {
  const validation = checkValidationArr(user_validation_arr)

  if (validation && !fetchingResource.value) {
    const json = getFormDataInJSONFormat('register_form')
    const response = await fetchResource('POST', json, '/register', 'api_key')

    if (response && response.ok) {
      alertSuccess()
      await _alert('Successfully registered account')

      // Storing login information, because some people struggle with remembering it

      const register_fields = JSON.parse(json)
      const new_username = register_fields.username
      const new_password = register_fields.password

      if (new_username) {
        username.value = new_username
        login_validation.Username = true

        password.value = new_password
        login_validation.Password = true
      }

      router.push({ name: 'macroLogin' })
    }
  } else {
    alertDanger()
    alertDanger()
    if (fetchingResource.value) {
      await _alert('Already registering...')
    } else {
      await _alert('Fill out the register fields correctly!')
    }
  }
}
</script>

<template>
  <div class="centerDiv">
    <div class="d-flex flex-column box">
      <WarningModule :message="warningMessage" />
      <AlertBox />
      <div class="card p-3 border border-1 shadow-lg">
        <div class="card-body d-flex flex-column justify-content-center">
          <h3 class="card-title">Register account:</h3>
          <form id="register_form" @submit.prevent>
            <RegisterModule />

            <div class="d-flex flex-row float-end">
              <template v-if="fetchingResource">
                <RequestLoader />
              </template>

              <button type="submit" class="btn btn-lg btn-primary m-2 me-0" @click="register()">
                Register
              </button>
            </div>

            <h5 class="mt-4 ms-2 mb-1">
              <RouterLink :to="{ name: 'macroLogin' }"> Login </RouterLink>
            </h5>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.centerDiv {
  display: flex;
  justify-content: center;

  margin-top: 2rem;
}

.box {
  width: clamp(350px, 15vw, 400px);
}
</style>
