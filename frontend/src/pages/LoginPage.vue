<template>
  <q-page padding>
    <q-card
      class="items-center my-card"
      style="width: 500px; left: calc(50% - 250px); top: 50px;"
    >
      <q-img src="~assets/Mountain.jpg" style="height: 200px"/>
      <div class="text-h4 text-center q-pa-md">登录</div>
      <q-card-section>
        <q-input
          class="q-my-sm"
          v-model="email"
          filled type="email"
          label="Email"
        />

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
            { label: '管理员登录', value: 'adminSignin' }
          ]"
        />
        <q-space />
        <q-btn
          class="q-ma-sm"
          v-close-popup
          color="primary"
          label="登录"
          @click="login" />
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
const isPwd = ref(true)


const login = () => {
  if (email.value === '' || password.value === '') {
    $q.notify('请输入邮箱和密码')
    return
  }
  if (inputType.value === 'adminSignin') {
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
      $userStore.login(res.data.id, res.data.email, res.data.username, "User")
      $router.push('/user')
      $q.notify('登录成功')
    }).catch((err) => {
      console.log(err)
      $q.notify('登录失败，账号不存在或密码错误')
    })
  }
}

</script>
