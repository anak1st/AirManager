<template>
  <q-page>
    <q-card
      class="items-center my-card"
      style="width: 400px; left: calc(50% - 200px); top: 80px;"
    >
      <q-img src="~assets/Mountain.jpg" style="height: 200px"/>

      <q-card-section>
        <div class="q-my-md text-h4 text-center">登录</div>

        <q-input
          class="q-my-sm"
          v-model="name"
          :disable="inputType !== 'userSignup'"
          filled type="text"
          label="用户名"
        />

        <q-input
          class="q-my-sm"
          v-model="email"
          filled type="email"
          label="Email" />

        <q-input
          class="q-my-sm"
          v-model="password"
          filled
          :type="isPwd ? 'password' : 'text'"
          label="密码"
        >
          <template v-slot:append>

            <q-icon
              :name="isPwd ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="isPwd = !isPwd"
            />
          </template>
        </q-input>

      </q-card-section>

      <q-separator />

      <q-card-actions>
        <q-btn-toggle
          v-model="inputType"
          class="q-ma-sm"
          toggle-color="primary"
          :options="[
            { label: '用户登录', value: 'userSignin' },
            { label: '用户注册', value: 'userSignup' },
            { label: '管理员登录', value: 'adminSignup' }
          ]"
        />
        <q-space></q-space>
        <q-btn
          class="q-mx-sm"
          v-close-popup
          v-if="inputType === 'userSignup'"
          color="primary"
          label="注册"
          @click="signup" />
        <q-btn
          class="q-ma-sm"
          v-close-popup
          v-if="inputType !== 'userSignup'"
          color="primary"
          label="登录"
          @click="signin" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup>

import { ref } from 'vue'
import { useQuasar } from 'quasar'
const $q = useQuasar()
import { useRouter } from 'vue-router'
const $router = useRouter()

import { useUserStore } from 'src/stores/user'
import { api } from 'src/boot/axios';
const $userStore = useUserStore()

const inputType = ref('userSignin')
const email = ref('')
const password = ref('')
const name = ref('')
const isPwd = ref(true)

const signup = () => {
  if (email.value === ''
   || password.value === ''
   || name.value === '') {
    $q.notify('请输入邮箱和密码')
    return
  }
  api.post('/users', {
    name: name.value,
    email: email.value,
    password: password.value,
  }).then((res) => {
    console.log(res)
    $q.notify('注册成功')
  }).catch((err) => {
    console.log(err)
    $q.notify('注册失败，请不要使用重复邮箱')
  })
}

const signin = () => {
  if (email.value === '' || password.value === '') {
    $q.notify('请输入邮箱和密码')
    return
  }

  if (inputType.value === 'adminSignup') {
    api.post('/admins/login', {
      email: email.value,
      password: password.value,
    }).then((res) => {
      console.log(res)
      if (res.data.admin_type === "Super") {
        $router.push('/manage')
      } else if (String(res.data.admin_type).startsWith("Airport")) {
        $router.push('/airport')
      } else if (String(res.data.admin_type).startsWith("Airline")) {
        $router.push('/company')
      } else {
        $q.notify('账号权限错误')
        return
      }
      $userStore.login(res.data.id, res.data.email, res.data.username, res.data.admin_type)
      $q.notify('登录成功')
    }).catch((err) => {
      console.log(err)
      $q.notify('登录失败，账号不存在或密码错误')
    })
  } else {
    api.post('/users/login', {
      email: email.value,
      password: password.value,
    }).then((res) => {
      console.log(res)
      $router.push('/')
      $userStore.login(res.data.id, res.data.email, res.data.name, "Null")
      $q.notify('登录成功')
    }).catch((err) => {
      console.log(err)
      $q.notify('登录失败，账号不存在或密码错误')
    })
  }
}

</script>
