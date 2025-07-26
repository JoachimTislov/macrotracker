<script setup lang="ts">
import {
  profilePictureUrl,
  userInfo,
  initPicture,
  recommended_nutrient_data,
  fetchingResource
} from '@/logic/initVariables'
import AlertBox from './Modules/AlertBox.vue'
import ChangePassword from './ChangePassword.vue'
import EditProfileInformation from './EditProfileModal.vue'
import { hideAlert } from '@/logic/alertFunctions'
import { onMounted } from 'vue'
import { getUserInfo } from '@/logic/Ajax/get/getUserInfo'
import BarChart from './BarChart.vue'
import RequestLoader from './RequestLoader.vue'

onMounted(async () => {
  await getUserInfo()
  await initPicture()
})
</script>

<template>
  <AlertBox />

  <ChangePassword />

  <EditProfileInformation />

  <div class="card">
    <section class="card-body">
      <div class="profileContainer d-flex">
        <div class="p-3 rounded d-flex flex-column mx-auto" style="width: 90%">
          <template v-if="fetchingResource && !userInfo">
            <div class="d-flex justify-content-center">
              <RequestLoader />
            </div>
          </template>

          <template v-else>
            <div class="d-flex p-1" v-for="(value, key) in userInfo" :key="key">
              <h3>{{ key }}:</h3>

              <h4 class="ms-auto">
                {{ value }}
                <template v-if="key == 'Weight'"> kg </template>
                <template v-if="key == 'Height'"> cm </template>
                <template v-if="key == 'Age'"> years old </template>
              </h4>
            </div>
          </template>
        </div>
        <div class="d-flex">
          <img :src="profilePictureUrl" alt="Could not load your picture" class="mx-auto rounded" />
        </div>
      </div>

      <div class="mt-3">
        <BarChart :data="recommended_nutrient_data" name="Recommended nutrient/macro consumption" />
      </div>

      <div class="d-flex">
        <div class="btn-group btn-group-md mt-4 ms-auto">
          <button type="button" class="btn btn-info" data-bs-toggle="modal" data-bs-target="#change_password_modal"
            @click="hideAlert()">
            Change password
          </button>
          <button type="button" class="btn btn-success" data-bs-toggle="modal"
            data-bs-target="#edit_profile_information_modal" @click="hideAlert()">
            Edit profile
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
img {
  width: clamp(300px, 33vw, 450px);
  max-height: clamp(300px, 33vw, 430px);
  object-fit: contain;
}

@media (max-width: 770px) {
  .profileContainer {
    flex-direction: column-reverse;
  }

  .marginBox {
    margin: 0;
  }
}

h4 {
  font-size: clamp(1rem, 2vw, 1.5rem);
}

h3 {
  font-weight: bolder;
  font-size: clamp(1.2rem, 2.2vw, 2rem);
}
</style>
