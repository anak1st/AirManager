<template>
  <DashboardLayout :page-list="UserLinks" page-title="User"  />
</template>

<script setup>
import DashboardLayout from './DashboardLayout.vue';
import { UserLinks } from 'src/router/links';

</script>

<style lang="scss">

</style>
