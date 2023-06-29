<template>
  <q-layout view="lHh lpR lff" class="bg-grey-4">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar class="bg-primary text-white">
        <q-btn @click="$router.push('/')">
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>

          <q-toolbar-title>Fly App</q-toolbar-title>
        </q-btn>
        <q-space />
        <q-btn icon="send"  class="q-ma-sm" label="注册" color="blue"  @click="$router.push('/register')"/>
        <q-btn icon="login" class="q-ma-sm" label="登录" color="green" @click="$router.push('/login')"/>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { useRouter } from 'vue-router';
const $router = useRouter();

</script>

<style lang="scss">

</style>
