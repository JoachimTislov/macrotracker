<script setup lang="ts">
import { validateGenderOrActivityLvl } from '@/logic/validation'
import { user_validation_arr, validation_messages } from '@/logic/initVariables'
import type { User_input_field, UserInfo } from '@/logic/types'
import { reactive, ref, watch } from 'vue'
import RegisterInputModule from './RegisterInputModule.vue'
import { user_id } from '@/logic/variables'

const props = defineProps<{
  user_info?: UserInfo
}>()

const _arr: User_input_field[] = reactive([
  {
    inputType: 'text',
    placeholder: '',
    validate_type: 'Username',
    identifier: 'username',
    class: 'input-group',
    attachment: 'Username:',
    type: 'prepend'
  },
  {
    inputType: 'password',
    placeholder: 'Password',
    validate_type: 'Password',
    identifier: 'password',
    class: 'form-group'
  },
  {
    inputType: 'password',
    placeholder: 'Repeat Password',
    validate_type: 'Password',
    identifier: 'confirm_password',
    class: 'form-group'
  },
  {
    inputType: 'text',
    placeholder: '',
    validate_type: 'Name',
    identifier: 'name',
    class: 'input-group',
    attachment: 'Name:',
    type: 'prepend'
  },
  {
    inputType: 'email',
    placeholder: '',
    validate_type: 'Email',
    identifier: 'email',
    class: 'input-group',
    attachment: '@ Email:',
    type: 'prepend'
  },
  {
    inputType: 'number',
    placeholder: 'Age',
    validate_type: 'Age',
    identifier: 'age',
    class: 'input-group',
    attachment: 'years old',
    type: 'append'
  },
  {
    inputType: 'number',
    placeholder: 'Height',
    validate_type: 'Height',
    identifier: 'height',
    class: 'input-group',
    attachment: 'cm',
    type: 'append'
  },
  {
    inputType: 'number',
    placeholder: 'Weight',
    validate_type: 'Weight',
    identifier: 'weight',
    class: 'input-group',
    attachment: 'kg',
    type: 'append'
  }
])

const selectedGender = ref<string>('0')
const selectedActivity_lvl = ref<string>('0')

watch(
  () => props.user_info,
  (newValue) => {
    if (newValue) {
      for (const key of Object.keys(user_validation_arr)) {
        user_validation_arr[key] = true
      }

      // Removing password entries
      if (_arr[1].identifier == 'password') {
        _arr.splice(1, 2)
      }

      if (user_id.value == '1' && _arr[0].identifier == 'username') {
        _arr.splice(0, 1)
      }

      for (const entry of _arr) {
        entry.value = newValue[entry.validate_type]
      }

      const activity_Levels: { [key: string]: string } = {
        Sedentary: '1',
        'Lightly Active': '2',
        'Moderately Active': '3',
        'Very Active': '4',
        'Super Active': '5'
      }

      selectedGender.value = newValue.Gender == 'Male' ? '1' : '2'
      selectedActivity_lvl.value = activity_Levels[newValue['Activity lvl']]
    }
  }
)
</script>

<template>
  <template v-for="entry in _arr" :key="entry.identifier">
    <RegisterInputModule :user_input_field="entry" />
  </template>

  <div class="input-group mt-2">
    <select @change="
      user_validation_arr.gender = validateGenderOrActivityLvl(
        $event,
        validation_messages.register.gender.value,
        'Gender',
        'form-control form-control-md'
      )
      " class="form-control form-control-md" name="gender" v-model="selectedGender" required>
      <option value="0">Choose Gender</option>
      <option value="1">Male</option>
      <option value="2">Female</option>
    </select>
    <div class="d-flex input-group-append">
      <span class="input-group-text"><font-awesome-icon :icon="['fas', 'person-half-dress']" /></span>
    </div>
    <div :ref="validation_messages.register.gender" class="ml-2 invalid-feedback" style="display: none"></div>
  </div>

  <div class="form-group mt-2">
    <select @change="
      user_validation_arr.activityLvl = validateGenderOrActivityLvl(
        $event,
        validation_messages.register.activity_lvl.value,
        'Activity Lvl',
        'form-control form-control-md'
      )
      " class="form-control form-control-md" name="activity_lvl" v-model="selectedActivity_lvl" required>
      <option value="0">Choose Activity Lvl</option>
      <option value="1">Sedentary</option>
      <option value="2">Lightly Active</option>
      <option value="3">Moderately Active</option>
      <option value="4">Very Active</option>
      <option value="5">Super Active</option>
    </select>
    <div :ref="validation_messages.register.activity_lvl" class="ml-2 invalid-feedback" style="display: none"></div>
  </div>
</template>
