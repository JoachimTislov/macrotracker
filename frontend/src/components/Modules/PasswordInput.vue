<script setup lang="ts">
import { change_password_validation } from '@/logic/initVariables'
import { ValidateText } from '@/logic/validation'
import { onMounted, ref } from 'vue'

const password_validation_message = ref<HTMLElement | null>(null)

onMounted(() => {
  password_validation_message.value?.focus()
})

defineProps<{
  password_details: { name: string; label: string }
}>()

const className = 'form-control form-control-md'
</script>

<template>
  <div class="mt-1">
    <label :for="password_details.name" class="form-label">
      {{ password_details.label }} Password:
    </label>
    <input @input="
      change_password_validation[password_details.name] = ValidateText(
        $event,
        password_validation_message,
        'Password',
        className
      )
      " :class="className" :name="password_details.name" type="password" placeholder="Password" />
    <div ref="password_validation_message" class="ml-3 invalid-feedback"></div>
  </div>
</template>
