<template>
  <q-page>
    <q-card
      class="items-center my-card"
      style="width: 400px; left: calc(50% - 200px); top: 50px;"
    >
      <q-img src="~assets/GawrGura.png" />

      <q-card-section>
        <div class="q-my-lg text-h4 text-center">登录</div>

        <q-input
          class="q-my-sm"
          v-model="email"
          filled type="email"
          hint="Email" />

        <q-input
          class="q-my-sm"
          v-model="password"
          filled
          :type="isPwd ? 'password' : 'text'"
          hint="密码"
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

      <q-card-actions align="right">
        <q-btn v-close-popup color="primary" label="注册" @click="signup" />
        <q-btn v-close-popup color="primary" label="登录" @click="signin" />
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

const email = ref('')
const password = ref('')
const isPwd = ref(true)

const signup = () => {
  if (email.value === '' || password.value === '') {
    $q.notify('请输入邮箱和密码')
    return
  }

  api.post('/users', {
    email: email.value,
    password: password.value,
  }).then((res) => {
    console.log(res)
    $q.notify('注册成功')
  }).catch((err) => {
    console.log(err)
    $q.notify('注册失败')
  })
}

const signin = () => {
  if (email.value === '' || password.value === '') {
    $q.notify('请输入邮箱和密码')
    return
  }

  api.post('/users/login', {
    email: email.value,
    password: password.value,
  }).then((res) => {
    console.log(res)
    $router.push('/')
    $userStore.login(res.data.id, res.data.email, res.data.name)
    $q.notify('登录成功')
  }).catch((err) => {
    console.log(err)
    $q.notify('登录成功')
  })
}

</script>
