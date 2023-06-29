<template>
  <q-page class="q-pa-lg">
    <h5>Airline Main Page</h5>
    <div>
      <div class="col">
        <div class="row" v-for="row of items" :key="row">
          <div class="items"
            v-for="col of row" :key="col"
          />
        </div>

      </div>
    </div>
    <div>
      {{ itemsCount }}
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const items = ref([])
const itemsCount = ref(0)
const itemsInit = () => {
  for (let i = 0; i < 7; i++) {
    items.value.push([])
    for (let j = 0; j < 55; j++) {
      items.value[i].push(j)
      itemsCount.value += 1
    }
  }
}

onMounted(() => {
  itemsInit()
})

</script>



<style>

.items {
  width: 12px;
  height: 12px;
  background-color: red;
  margin: 1px;
}

</style>

