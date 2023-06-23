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
          Quasar App
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
      <div class="q-px-xl q-pt-xl q-pb-md">
        <div class="text-h3 text-weight-bold">
          Todo
        </div>
        <div class="text-subtitle1">{{ todayDate }}</div>
      </div>
      <q-img
        src="~assets/GawrGura.png"
        class="header-image absolute-top"
      />

    </q-header>

    <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        :width="300"
        :breakpoint="600"
      >
        <q-scroll-area
          style="height: calc(100% - 192px); margin-top: 192px; border-right: 1px solid #ddd">
          <q-list padding>
            <q-item
              to="/"
              exact
              clickable
              v-ripple>
              <q-item-section avatar>
                <q-icon name="list" />
              </q-item-section>

              <q-item-section>
                Todo
              </q-item-section>
            </q-item>

            <q-item
              to="/help"
              exact
              clickable
              v-ripple>
              <q-item-section avatar>
                <q-icon name="help" />
              </q-item-section>

              <q-item-section>
                帮助
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

        <q-img class="absolute-top" src="~assets/CatGirl.png" style="height: 192px">
          <div class="absolute-bottom bg-transparent">
            <q-avatar size="56px" class="q-mb-sm">
              <img src="~assets/heita2.jpg">
            </q-avatar>
            <div class="word-shadow text-h5 text-weight-bold text-grey-9"> {{ $userStore.name }}  </div>
            <div class="word-shadow text-grey-9"> {{ $userStore.email }}</div>
          </div>
        </q-img>
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

const timer = setInterval(() => {
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

</script>

<style lang="scss">
.header-image {
  height: 100%;
  z-index: -1;
  opacity: 0.4;
  filter: grayscale(60%);
}

.avatar-image {
  filter: brightness(60%);
}

.word-shadow {
  text-shadow: 0 0 10px #ffffff,
               0 0 20px #ffffff,
               0 0 30px #ffffff,
               0 0 40px #ffffff,
}
</style>
