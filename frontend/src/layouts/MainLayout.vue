<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Fly App
        </q-toolbar-title>
      </q-toolbar>
      <div class="q-px-xl q-pt-xl q-pb-md">
        <div class="text-h3 text-weight-bold q-mr-md">
          {{ pageTitle }}
        </div>
        <div class="text-subtitle1">{{ todayDate }}</div>
      </div>
      <q-img
        src="src/assets/A380.jpg"
        class="header-image absolute-top"
      />

    </q-header>

    <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        :width="300"
        :breakpoint="600"
      >
        <q-img
          src="~assets/Mountain.jpg"
          class="absolute-top"
          style="height: 192px"
        >
          <q-item class="absolute-bottom">
            <q-item-section avatar>
              <q-avatar size="56px" color="white">
                <img v-if = "avatarImage.length !== 0" :src="avatarImage" >
                <div class="text-black" v-if = "avatarImage.length === 0">
                  {{ ($userStore.username.length > 0 ? $userStore.username : "虚无")[0] }}
                </div>
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <div class="word-shadow text-h6 text-weight-bold">
                {{ $userStore.username.length > 0 ? $userStore.username : "虚无" }}
              </div>
              <div class="word-shadow text-subtitle2">
                {{ $userStore.email.length > 0 ? $userStore.email : "123456@nullptr.com" }}
              </div>
            </q-item-section>
          </q-item>
        </q-img>

        <q-scroll-area
          style="height: calc(100% - 192px); margin-top: 192px; border-right: 1px solid #ddd">
          <q-list padding>

            <q-item v-for="page in pageList" :key="page.to"
              :to="page.to"
              exact
              clickable
              v-ripple>
              <q-item-section avatar>
                <q-icon :name="page.icon" />
              </q-item-section>

              <q-item-section>
                {{ page.text }}
              </q-item-section>
            </q-item>

            <q-separator spaced />

            <q-item
              exact
              clickable
              @click="confirm"
              v-ripple>
              <q-item-section avatar>
                <q-icon name="logout" />
              </q-item-section>

              <q-item-section>
                注销
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { date } from 'quasar'

import { useQuasar } from 'quasar';
const $q = useQuasar()

import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()

import { useRouter } from 'vue-router';
const $router = useRouter()

const leftDrawerOpen = ref(false)
const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

const todayDate = ref(date.formatDate(Date.now(), 'YYYY/MM/DD HH:mm:ss'))

setInterval(() => {
  todayDate.value = date.formatDate(Date.now(), 'YYYY/MM/DD HH:mm:ss')
}, 1000)

const confirm = () => {
  $q.dialog({
    title: '确认',
    message: '你真的要注销吗?',
    cancel: '取消',
    ok: '确定',
    persistent: true
  }).onOk(() => {
    $userStore.logout()
    $router.push('/login')
  })
}

const avatarImage = ref('')

defineProps({
  pageList: { type: Array },
  pageTitle: { type: String }
})

</script>

<style lang="scss">
.header-image {
  height: 100%;
  z-index: -1;
  opacity: 0.4;
  filter: grayscale(60%);
}
</style>
