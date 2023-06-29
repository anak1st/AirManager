<template>
  <q-page>
    <q-list bordered>
      <q-item
        v-for="flight in flights"
        :key="flight.id"
        class="q-my-sm row"
        clickable
        @click="clickModify(flight.id)"
        v-ripple
      >
        <q-item-section class="col-1">
          <q-avatar color="primary" text-color="white">
            <q-item-label>{{ flight.aircraft.airline.name[0] }}</q-item-label>
          </q-avatar>
        </q-item-section>

        <q-item-section class="col-2">
          <q-item-label>
            {{ flight.aircraft.airline.code + " " + flight.id + " " + flight.aircraft.type.name }}
          </q-item-label>
          <q-item-label caption>{{ flight.aircraft.airline.name }}</q-item-label>
        </q-item-section>

        <q-item-section class="col-2 items-end">
          <q-item-label>{{ getTime(flight.time_departure) }}</q-item-label>
          <q-item-label caption>{{ flight.flight_type.airport_departure.name }}</q-item-label>
          <q-item-label caption>{{ flight.flight_type.airport_departure.code }}</q-item-label>

        </q-item-section>

        <q-item-section class="col-1">
          <q-item-label caption>
            {{ getCostTime(flight.time_departure, flight.time_arrival) }}
          </q-item-label>
          <q-item-label>
            <q-img src="~assets/arrow.png"  />
          </q-item-label>
        </q-item-section>

        <q-item-section class="col-2">
          <q-item-label>{{ getTime(flight.time_arrival) }}</q-item-label>
          <q-item-label caption>{{ flight.flight_type.airport_arrival.name }}</q-item-label>
          <q-item-label caption>{{ flight.flight_type.airport_arrival.code }}</q-item-label>

        </q-item-section>

        <q-item-section class="col-1" side>
          <q-item-label>{{ getStatus(flight.status) }}</q-item-label>
        </q-item-section>

        <q-item-section class="col-2" side>
          <q-item-label>已售 ? 张</q-item-label>
          <q-item-label caption>已售 ? 元</q-item-label>
        </q-item-section>

      </q-item>
    </q-list>
    <q-dialog v-model="card" >
      <q-card class="my-card" style="width: 400px;">

        <q-card-section>
          <div class="q-my-md text-h5 text-center"> {{ cardStatus }}航班信息 </div>


          <q-input filled class="q-ma-md" v-model="aircraft_id" label="飞机代码" />

          <q-select filled class="q-ma-md" v-model="flight_type_id" :options="flight_types" label="出发机场" />

          <q-input filled label="出发时间" class="q-ma-md" v-model="time_departure">
            <template v-slot:append>
              <q-icon name="event" class="q-px-sm cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-date v-model="time_departure" mask="YYYY-MM-DD HH:mm">
                    <div class="row items-center justify-end">
                      <q-btn v-close-popup label="Close" color="primary" flat />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-icon>
              <q-icon name="access_time" class="q-px-sm cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-time v-model="time_departure" mask="YYYY-MM-DD HH:mm" format24h>
                    <div class="row items-center justify-end">
                      <q-btn v-close-popup label="Close" color="primary" flat />
                    </div>
                  </q-time>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>

          <q-input filled label="到达时间" class="q-ma-md" v-model="time_arrival">
            <template v-slot:append>
              <q-icon name="event" class="q-px-sm cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-date v-model="time_arrival" mask="YYYY-MM-DD HH:mm">
                    <div class="row items-center justify-end">
                      <q-btn v-close-popup label="Close" color="primary" flat />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-icon>
              <q-icon name="access_time" class="q-px-sm cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-time v-model="time_arrival" mask="YYYY-MM-DD HH:mm" format24h>
                    <div class="row items-center justify-end">
                      <q-btn v-close-popup label="Close" color="primary" flat />
                    </div>
                  </q-time>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>

          <q-option-group
            v-model="group"
            :options="options"
            color="primary"
            inline
          />
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn v-close-popup color="primary" label="取消" />
          <q-btn v-close-popup color="primary" :label="cardStatus" @click="confirm" />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn
        fab
        icon="add"
        color="accent"
        @click="clickAdd"
      />
    </q-page-sticky>
  </q-page>
</template>

<script setup>
import { date, useQuasar } from 'quasar';
const $q = useQuasar()
import { onMounted, ref } from 'vue'
import { api } from 'src/boot/axios';
import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()

const flights = ref([])
let flight_types = []

const updateFlightTypes = () => {
  const airline_code = $userStore.admin_type.slice(8)
  const url = '/flight_types/airline_code/' + airline_code
  api.get(url).then((res) => {
    flight_types = res.data
    for (let flight_type of flight_types) {
      flight_type.label = ' (' + flight_type.id + ') ' + flight_type.airport_departure.city + " -> " + flight_type.airport_arrival.city
      flight_type.value = flight_type.id
    }
  })
}


const updateFlights = () => {
  const url = '/flights/airline_code/' + $userStore.admin_type.slice(8)
  api.get(url).then((res) => {
    flights.value = res.data
  })
}

const getTime = (ISOTime) => {
  const LocaleString = new Date(ISOTime).toLocaleString()
  const GoodLocaleString = date.formatDate(LocaleString, 'M月D日 HH:mm')
  return GoodLocaleString
}
const getCostTime = (time_departure, time_arrival) => {
  const cost = new Date(time_arrival) - new Date(time_departure)
  const hour = Math.floor(cost / 1000 / 60 / 60)
  const minute = Math.floor(cost / 1000 / 60) - hour * 60

  return hour + "小时" + minute + "分钟"
}
const getStatus = (status) => {
  if (status === 'cancel') {
    return '取消'
  } else if (status === 'delay') {
    return '延误'
  }
  return '准点'
}


const aircraft_id = ref('')
const flight_type_id = ref('')
const time_departure = ref('')
const time_arrival = ref('')
let modify_id = 0
const group = ref('normal')
const options = [
  {
    label: '准点',
    value: 'normal'
  },
  {
    label: '延误',
    value: 'delay'
  },
  {
    label: '取消',
    value: 'cancel'
  }
]

const card = ref(false)
const cardStatus = ref("")

const clickAdd = () => {
  card.value = true
  cardStatus.value = "添加"
}
const clickModify = (id) => {
  modify_id = id
  card.value = true
  cardStatus.value = "修改"

  const flight = flights.value.filter((flight) => flight.id === id)[0]
  aircraft_id.value = flight.aircraft_id
  flight_type_id.value = flight.flight_type_id
  time_departure.value = date.formatDate(flight.time_departure, 'YYYY-MM-DD HH:mm')
  time_arrival.value = date.formatDate(flight.time_arrival, 'YYYY-MM-DD HH:mm')
  group.value = flight.status
}

const confirm = () => {
  if (cardStatus.value === "添加") {
    confirmAdd()
  } else {
    confirmModify()
  }
}

const confirmAdd = () => {
  const url = '/flights/'
  const data = {
    aircraft_id: aircraft_id.value,
    flight_type_id: flight_type_id.value,
    time_departure: time_departure.value,
    time_arrival: time_arrival.value,
    status: group.value
  }
  api.post(url, data).then((res) => {
    updateFlights()
    addFlightsCard.value = false
    $q.notify({
      color: 'green-4',
      textColor: 'white',
      icon: 'cloud_done',
      message: '添加成功!',
    })
  }).catch((err) => {
    console.log(err)
    $q.notify({
      color: 'red-4',
      textColor: 'white',
      icon: 'cloud_done',
      message: '添加失败!',
    })
  })
}

const confirmModify = () => {
  const url = '/flights/id/' + modify_id
  const data = {
    aircraft_id: aircraft_id.value,
    flight_type_id: flight_type_id.value,
    time_departure: time_departure.value,
    time_arrival: time_arrival.value,
    status: group.value
  }
  api.put(url, data).then((res) => {
    updateFlights()
    addFlightsCard.value = false
    $q.notify({
      color: 'green-4',
      textColor: 'white',
      icon: 'cloud_done',
      message: '修改成功!',
    })
  }).catch((err) => {
    console.log(err)
    $q.notify({
      color: 'red-4',
      textColor: 'white',
      icon: 'cloud_done',
      message: '修改失败!',
    })
  })
}


const updateAll = () => {
  updateFlights()
  updateFlightTypes()
}
onMounted(() => {
  updateAll()
})
setInterval(async () => {
  await updateAll()
  console.log(flights.value)
}, 1000 * 10);


</script>
