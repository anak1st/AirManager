<template>
  <q-page>
    <q-list bordered>
      <q-item
        v-for="flight_type in flight_types"
        :key="flight_type.id"
        class="q-my-sm row"
        clickable

        v-ripple
      >
        <q-item-section class="">
          <q-item-label>{{ flight_type.airline_code + " " + flight_type.id }}</q-item-label>
        </q-item-section>

        <q-item-section class=" items-end">
          <q-item-label>{{ flight_type.airport_departure.name }}</q-item-label>
        </q-item-section>

        <q-item-section class="q-px-md ">
          <q-item-label caption>
            {{ "lat: " + String(flight_type.airport_departure.lat).slice(0, 10) }}
          </q-item-label>
          <q-item-label caption>
            {{ "lng: " + String(flight_type.airport_departure.lng).slice(0, 10) }}
          </q-item-label>
        </q-item-section>

        <q-item-section class="">
          <q-item-label caption>
            {{ flight_type.distence }}
          </q-item-label>
          <q-item-label>
            <q-img src="~assets/arrow4.png"  />
          </q-item-label>
        </q-item-section>

        <q-item-section class="q-px-md items-end">
          <q-item-label caption>
            {{ "lat: " + String(flight_type.airport_arrival.lat).slice(0, 10) }}
          </q-item-label>
          <q-item-label caption>
            {{ "lng: " + String(flight_type.airport_arrival.lng).slice(0, 10) }}
          </q-item-label>
        </q-item-section>

        <q-item-section class="">
          <q-item-label>{{ flight_type.airport_arrival.name }}</q-item-label>
        </q-item-section>

        <q-item-section class="" side>
          <q-btn round color="red" icon="delete" @click="confirm(flight_type.id)" />
        </q-item-section>
      </q-item>
    </q-list>
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn
        fab
        icon="add"
        color="accent"
        @click="cardAdd = true"
      />
    </q-page-sticky>
    <q-dialog v-model="cardAdd" >
      <q-card class="my-card" style="width: 400px;">
        <q-card-section>
          <div class="q-my-md text-h4 text-center"> 添加一条航班类型! </div>

          <q-select filled class="q-ma-md" v-model="selected1" :options="airports" label="出发机场" />
          <q-select filled class="q-ma-md" v-model="selected2" :options="airports" label="到达机场" />

          <div class="q-ma-md"> {{ dis }} </div>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn v-close-popup color="primary" label="取消" />
          <q-btn v-close-popup color="primary" label="添加" @click="addFlightType" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { useQuasar } from 'quasar';
const $q = useQuasar()
import { onMounted, ref, watch } from 'vue'
import { api } from 'src/boot/axios';
import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()

const notify_success = (message) => {
  $q.notify({
    message: message,
    color: "green",
    icon: "check",
  });
}

const notify_error = (message) => {
  $q.notify({
    message: message,
    color: "red",
    icon: "close",
  });
}

const flight_types = ref([])
let airports = []
const selected1 = ref([])
const selected2 = ref([])
const dis = ref("")

const updateFlightTypes = () => {
  const airline_code = $userStore.admin_type.slice(8)
  const url = '/flight_types/airline_code/' + airline_code
  api.get(url).then(async (res) => {
    flight_types.value = res.data
    for (let flight_type of flight_types.value) {
      flight_type.distence = await distence(flight_type.airport_code_departure, flight_type.airport_code_arrival)
      flight_type.distence = String(flight_type.distence).slice(0, 6) + " (km)"
    }
  })
}

const updateAirports = () => {
  const url = '/airports'
  api.get(url).then((res) => {
    airports = res.data
    for (let airport of airports) {
      airport.label = airport.name + ' (' + airport.code + ')'
      airport.value = airport.code
    }
  })
}

const distence = async (airport1_code, airport2_code) => {
  const url = '/airports/dis/'
  const res = await api.get(url, { params: {
    airport1_code: airport1_code,
    airport2_code: airport2_code,
  }})
  return res.data
}

const updateSelectedDistence = async () => {
  if (selected1.value.length == 0 || selected2.value.length == 0) {
    dis.value = "请输入机场代码!"
    return
  }

  dis.value = await distence(selected1.value.code, selected2.value.code)
  dis.value = "距离: " + String(dis.value).slice(0, 6) + " (km)"
}


const cardAdd = ref(false)

const addFlightType = () => {
  if (dis.value < 100) {
    notify_error("距离过近!")
    return
  }
  const airline_code = $userStore.admin_type.slice(8)
  api.post('/flight_types', {
    airline_code: airline_code,
    airport_code_departure: selected1.value.code,
    airport_code_arrival: selected2.value.code,
  }).then((res) => {
    notify_success("添加成功!")
    updateFlightTypes()
  }).catch((err) => {
    console.log(err)
    notify_error("添加失败!")
  })
}

const confirm = (id) => {
  $q.dialog({
    title: '确认',
    message: '你真的要删除吗?',
    cancel: '取消',
    ok: '确定',
    persistent: true
  }).onOk(() => {
    api.delete('/flight_types/id/' + id).then((res) => {
      notify_success("删除成功!")
      updateFlightTypes()
    }).catch((err) => {
      notify_error("删除失败!")
      console.log(err)
    })
  })
}

watch(selected1, () => {
  updateSelectedDistence()
})
watch(selected2, () => {
  updateSelectedDistence()
})

const updateAll = () => {
  updateAirports()
  updateFlightTypes()
  updateSelectedDistence()
}
onMounted(() => {
  updateAll()
})
setInterval(() => {
  updateAll()
}, 1000 * 10);


</script>
