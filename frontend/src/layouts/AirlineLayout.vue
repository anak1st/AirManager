<template>
  <DashboardLayout :page-list="AirlineLinks" page-title="Airline"  />
</template>

<script setup>
import DashboardLayout from './DashboardLayout.vue';
import { AirlineLinks } from 'src/router/links';

</script>

<style lang="scss">

</style>
