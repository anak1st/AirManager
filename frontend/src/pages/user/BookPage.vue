<template>
  <q-page class="q-pa-lg">
    <h5>User Main Page</h5>
  </q-page>
</template>

<script setup>

import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()
import { onMounted, ref } from 'vue';
import { api } from 'src/boot/axios';

const books = ref([])
const updateBooks = () => {
  const url = '/books/user/' + $userStore.id
  return api.get(url).then((res) => {
    books.value = res.data
    console.log(books.value)
  })
}

onMounted(() => {
  updateBooks()
})

setInterval(() => {
  updateBooks()
}, 1000 * 20);

</script>
