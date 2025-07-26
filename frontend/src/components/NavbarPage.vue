<script setup lang="ts">
import { removeLocalData, fetchResource } from '@/logic/Ajax/ajax'
import { username, token } from '@/logic/variables'
import { _alert, alertSecondary } from '@/logic/alertFunctions'
import router from '@/router'

const logout = async () => {
  removeLocalData()
  await fetchResource('POST', '', '/logout', 'token')

  // assuming the logout is successful, backend deletes the token or session key from the database, preventing
  // third party member to exploit the token

  alertSecondary()
  await _alert('Successfully logged you out')

  router.push({ name: 'macroLogin' })
}

const routes = ['Home', 'Calender', 'Meals', 'Ingredients', 'Profile']
</script>

<template>
  <nav v-if="token" class="navbar navbar-expand-md" data-bs-theme="dark">
    <div class="container">
      <h4 class="logo">{{ username }}</h4>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMacroTracker"
        aria-controls="navbarMacroTracker" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarMacroTracker">
        <ul class="navbar-nav me-auto">
          <li class="nav-item" v-for="route in routes" :key="route">
            <RouterLink class="nav-link" :to="{ name: `macro${route}` }">
              {{ route }}
            </RouterLink>
          </li>
        </ul>

        <button @click="logout()" class="btn btn-outline-danger btn-lg">Log out</button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.logo {
  margin: 0;
  margin-right: 2rem;
}

li {
  font-size: large;
}
</style>
