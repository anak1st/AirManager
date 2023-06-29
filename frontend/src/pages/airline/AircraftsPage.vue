<template>
  <q-page class="q-pa-lg bg-grey-1 column">
    <div>
      <q-table
        flat bordered
        :rows="aircrafts"
        :columns="aircraftColumns"
        row-key="name"
        selection="single"
        v-model:selected="aircraftSelected"
        separator="cell"
      />
      <q-btn-group class="q-my-md">
        <q-btn color="accent" icon="card_giftcard" label="添加" />
        <q-btn color="accent" icon="create" label="删除">
          : {{ "无" }}
        </q-btn>
      </q-btn-group>
    </div>
    <q-dialog v-model="addAircraftCard" >
      <q-card class="my-card" style="width: 400px;">
        <q-img src="~assets/A380.jpg" style="height: 150px;" />

        <q-card-section>
          <div class="q-my-md text-h4 text-center"> 添加机场管理员 </div>

          <q-input filled class="q-ma-md" v-model="addAircraftCard" label="密码"   />
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn v-close-popup color="primary" label="取消" />
          <q-btn v-close-popup color="primary" label="添加" @click="addAdmin" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from 'src/boot/axios';
import { useQuasar } from 'quasar';
const $q = useQuasar()
import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()


const aircrafts = ref([])
const aircraftSelected = ref([])
const aircraftColumns = [
  {
    name: 'id',
    required: true,
    label: 'ID',
    align: 'left',
    field: 'id',
    sortable: true
  },
  {
    name: 'flightCount',
    align: 'left',
    label: '航班数量',
    field: row => row.flights.length,
    sortable: true
  },
  {
    name: 'type',
    align: 'left',
    label: '飞机型号',
    field: row => row.type.name,
    sortable: true
  },
  {
    name: 'seatCount',
    align: 'left',
    label: '座位数量',
    field: row => JSON.parse(row.type.model).seat_number,
    sortable: true
  },
]

const getAirlineCode = () => {
  // console.log($userStore.admin_type)
  return $userStore.admin_type.slice(8)
}

const updateAirports = () => {
  // console.log(getAirlineCode())
  const url = '/aircrafts/airline_code/' + getAirlineCode()
  api.get(url).then((res) => {
    aircrafts.value = res.data
    console.log(res.data)
  })
}

const addAircraftCard = ref(false)

const updateAll = () => {
  updateAirports()
}
onMounted(() => {
  updateAll()
})
// every 10s update
setInterval(() => {
  updateAll()
}, 1000 * 10)

</script>

<style lang="scss">

</style>
