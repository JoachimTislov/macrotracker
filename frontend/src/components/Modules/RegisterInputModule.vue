<script setup lang="ts">
import type { User_input_field } from '@/logic/types'
import { ValidateText } from '@/logic/validation'
import { ref } from 'vue'
import { user_validation_arr } from '@/logic/initVariables'

const input_validation_message = ref<HTMLElement | null>(null)

defineProps<{
  user_input_field: User_input_field
}>()
</script>

<template>
  <div class="mt-2" :class="user_input_field.class">
    <div v-if="user_input_field.type && user_input_field.type == 'prepend'"
      :class="`input-group-${user_input_field.type}`">
      <span class="input-group-text"> {{ user_input_field.attachment }} </span>
    </div>
    <input @input="
      user_validation_arr[user_input_field.identifier] = ValidateText(
        $event,
        input_validation_message,
        user_input_field.validate_type,
        'form-control form-control-md'
      )
      " class="form-control form-control-md" :type="user_input_field.inputType"
      :placeholder="user_input_field.placeholder" :value="user_input_field.value" :name="user_input_field.identifier"
      required />
    <div v-if="user_input_field.type && user_input_field.type == 'append'"
      :class="`input-group-${user_input_field.type}`">
      <span class="input-group-text"> {{ user_input_field.attachment }} </span>
    </div>
  </div>
  <div ref="input_validation_message" class="ml-2 invalid-feedback" style="display: none"></div>
</template>
