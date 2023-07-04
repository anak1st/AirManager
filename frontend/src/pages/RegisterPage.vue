<template>
  <q-page padding>
    <q-card
      class="items-center my-card"
      style="top: 50px; width: 500px; left: calc(50% - 250px);"
    >
      <q-img src="~assets/Mountain.jpg" style="height: 200px"/>
      <div class="text-h4 text-center q-pa-md">注册</div>
      <q-stepper
        v-model="step"
        vertical
        color="primary"
        animated
      >
        <q-step
          :name="1"
          title="登陆信息"
          icon="add"
          :done="step > 1"
        >
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
          <q-stepper-navigation>
            <q-btn @click="gotoStep2" color="primary" label="继续" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="2"
          title="个人信息"
          icon="add"
          :done="step > 2"
        >
          <q-input
            class="q-my-sm"
            v-model="username"
            filled type="text"
            label="用户名"
          />

          <q-input
            class="q-my-sm"
            v-model="fullname"
            filled type="text"
            label="真实姓名"
          />

          <q-input
            class="q-my-sm"
            v-model="phone"
            filled type="text"
            label="手机号"
          />

          <q-input
            class="q-my-sm"
            v-model="address"
            filled type="text"
            label="居住地址"
          />

          <q-stepper-navigation>
            <q-btn @click="step = 3" color="primary" label="继续" />
            <q-btn flat @click="step = 1" color="primary" label="返回" class="q-ml-sm" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="3"
          title="完成注册"
          icon="send"
        >
          <div> 完成注册代表您同意本应用的用户协议 </div>
          <q-stepper-navigation>
            <q-btn @click="register" color="primary" label="注册" />
            <q-btn flat @click="step = 2" color="primary" label="返回" class="q-ml-sm" />
          </q-stepper-navigation>
        </q-step>
      </q-stepper>
    </q-card>
    <div style="height: 100px;">

    </div>
  </q-page>
</template>

<script setup>

import { ref } from 'vue'
import { useQuasar } from 'quasar'
const $q = useQuasar()
import { useRouter } from 'vue-router'
const $router = useRouter()

import { api } from 'src/boot/axios';

const notify_sucess = (message) => {
  $q.notify({
    message: message,
    color: "green",
    icon: "check",
  });
}

const notify_error = (message) => {
  $q.notify({
    message: message,
    color: "red",
    icon: "close",
  });
}

const step = ref(1)

const email = ref('')
const password = ref('')
const isPwd = ref(true)

const username = ref('')
const fullname = ref('')
const phone = ref('')
const address = ref('')

const gotoStep2 = () => {
  if (email.value === ''
   || password.value === '') {
    notify_error('请输入邮箱和密码')
    return
  }
  step.value = 2
}

const gotoStep3 = () => {
  if (username.value === '') {
    notify_error('请输入用户名')
    return
  }
  if (fullname.value === '') {
    notify_error('请输入全名')
    return
  }
  if (phone.value === '') {
    notify_error('请输入手机号')
    return
  }
  if (address.value === '') {
    notify_error('请输入居住地址')
    return
  }
  step.value = 3
}

const register = () => {
  api.post('/users', {
    email: email.value,
    password: password.value,
    username: username.value,
    fullname: fullname.value,
    phone: phone.value,
    address: address.value,
  }).then((res) => {
    notify_sucess('注册成功')
    $router.push('/')
  }).catch((err) => {
    console.log(err)
    notify_error('注册失败')
  })
}
</script>
