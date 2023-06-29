<template>
  <DashboardLayout :page-list="AirportLinks" page-title="Airport"  />
</template>

<script setup>
import DashboardLayout from './DashboardLayout.vue';
import { AirportLinks } from 'src/router/links';

</script>

<style lang="scss">

</style>
