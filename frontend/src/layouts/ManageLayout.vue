<template>
  <MainLayout
  :page-list="ManageLinks"
  page-title="Manage"
/>
</template>

<script setup>

// import { useUserStore } from 'src/stores/user';
// const $userStore = useUserStore();

import MainLayout from './MainLayout.vue';
import { ManageLinks } from 'src/router/links';

</script>

<style lang="scss">

</style>
