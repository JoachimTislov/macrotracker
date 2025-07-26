<script setup lang="ts">
import { RouterLink } from 'vue-router'
import {
  validation_messages,
  login_validation,
  password,
  fetchingResource,
  warningMessage
} from '@/logic/initVariables'
import { ValidateText } from '@/logic/validation'

import AlertBox from './Modules/AlertBox.vue'
import { username } from '@/logic/variables'
import RequestLoader from './RequestLoader.vue'
import WarningModule from './Modules/WarningModule.vue'
import { login } from '@/logic/Ajax/login'
import { initiateExampleAccount } from '@/logic/initiateExampleAccount'
</script>

<template>
  <div class="centerDiv">
    <div class="d-flex flex-column box">
      <WarningModule class="mt-2" :message="warningMessage" />
      <AlertBox />
      <div class="card p-3 border border-1 shadow-lg">
        <div class="card-body">
          <h2 class="card-title">Macro Tracker</h2>

          <form @submit.prevent>
            <div class="form-group">
              <input @input="
                login_validation.Username = ValidateText(
                  $event,
                  validation_messages.login.username.value,
                  'Username',
                  'form-control form-control-lg'
                )
                " class="form-control form-control-lg" type="text" v-model="username" placeholder="Username"
                required />
              <div :ref="validation_messages.login.username" class="ml-3 invalid-feedback" style="display: none"></div>
            </div>

            <div class="form-group">
              <input @input="
                login_validation.Password = ValidateText(
                  $event,
                  validation_messages.login.password.value,
                  'Password',
                  'mt-2 form-control form-control-lg'
                )
                " class="mt-2 form-control form-control-lg" type="password" v-model="password" placeholder="Password"
                required />
              <div :ref="validation_messages.login.password" class="ml-3 mb-1 invalid-feedback" style="display: none">
              </div>
            </div>

            <RouterLink class="btn-link" :to="{ name: 'macroRegister' }">
              Register an account
            </RouterLink>

            <div class="d-flex flex-column">
              <div class="ms-auto d-flex align-items-center">
                <template v-if="fetchingResource">
                  <RequestLoader />
                </template>

                <button type="submit" class="btn btn-lg btn-primary" @click="login()">Login</button>
              </div>
            </div>
          </form>
        </div>
      </div>

      <div class="d-flex">
        <button type="submit" class="d-flex align-items-center justify-content-center m-2 ms-0 btn btn-lg btn-secondary"
          @click="initiateExampleAccount()">
          <font-awesome-icon class="me-1" :icon="['fas', `arrow-right`]" />
          Go to example account
        </button>
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
  width: 330px;
}
</style>
