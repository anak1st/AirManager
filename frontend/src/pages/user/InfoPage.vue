<template>
  <q-page>
    <q-card class="q-pa-md q-ma-md" style="max-width: 600px;">
      <h5>个人信息</h5>
      <q-input
        class="q-mb-md"
        v-model="username"
        filled type="text"
        label="用户名"
      />

      <q-input
        class="q-my-md"
        v-model="fullname"
        filled type="text"
        label="真实姓名"
      />

      <q-input
        class="q-my-md"
        v-model="phone"
        filled type="text"
        label="手机号"
      />

      <q-input
        class="q-my-md"
        v-model="address"
        filled type="text"
        label="居住地址"
      />

      <q-btn class="q-my-sm" @click="modifyUserInfo" color="primary" label="需改" />
    </q-card>

    <q-card class="q-pa-md q-ma-md" style="max-width: 600px;">
      <h5>密码</h5>
      <q-input
        class="q-my-sm"
        v-model="password1"
        filled
        :type="isPwd1 ? 'password' : 'text'"
        label="请输入密码"
      >
        <template v-slot:append>

          <q-icon
            :name="isPwd1 ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd1 = !isPwd1"
          />
        </template>
      </q-input>

      <q-input
        class="q-my-sm"
        v-model="password2"
        filled
        :type="isPwd2 ? 'password' : 'text'"
        label="请再输一遍密码"
      >
        <template v-slot:append>

          <q-icon
            :name="isPwd2 ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd2 = !isPwd2"
          />
        </template>
      </q-input>

      <q-btn class="q-my-sm" @click="modifyPasswd" color="primary" label="修改密码" />
    </q-card>
  </q-page>
</template>

<script setup>

import { onMounted, ref } from 'vue'
import { api } from 'src/boot/axios';
import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()
import { useQuasar } from 'quasar';
const $q = useQuasar()
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

const username = ref('')
const fullname = ref('')
const phone = ref('')
const address = ref('')


const updateUserInfo = () => {
  const url = 'users/id/' + $userStore.id
  api.get(url).then((res) => {
    username.value = res.data.username
    fullname.value = res.data.fullname
    phone.value = res.data.phone
    address.value = res.data.address
  })
}


const modifyUserInfo = () => {
  $q.dialog({
    title: '更新',
    message: '确定更新个人信息吗?',
    ok: '确定',
    cancel: '取消',
    persistent: true,
  }).onOk(() => {
    const url = 'users/id/' + $userStore.id
    api.put(url, {
      username: username.value,
      fullname: fullname.value,
      phone: phone.value,
      address: address.value,
    }).then((res) => {
      updateUserInfo()
      notify_sucess('更新成功')
    }).catch((err) => {
      console.log(err)
      notify_error('更新失败')
    })
  })
}

const password1 = ref('')
const password2 = ref('')
const isPwd1 = ref(true)
const isPwd2 = ref(true)


const modifyPasswd = () => {
  if (password1.value.length < 6) {
    notify_error('密码长度不能小于6')
    return
  }

  if (password1.value != password2.value) {
    notify_error('两次输入的密码不一致')
    return
  }
  $q.dialog({
    title: '更新',
    message: '确定更新密码吗?',
    ok: '确定',
    cancel: '取消',
    persistent: true,
  }).onOk(() => {
    const url = 'users/passwd/id/' + $userStore.id
    const email = $userStore.email
    api.put(url, {
      email: email,
      password: password1.value,
    }).then((res) => {
      notify_sucess('更新成功')
    }).catch((err) => {
      console.log(err)
      notify_error('更新失败')
    })
  })
}


onMounted(() => {
  updateUserInfo()
})

setInterval(() => {
  updateUserInfo()
}, 1000*60);


</script>
