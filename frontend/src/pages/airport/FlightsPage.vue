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
        <q-item-section avatar>
          <q-avatar color="primary" text-color="white">
            <q-item-label>{{ flight.aircraft.airline.name[0] }}</q-item-label>
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label>
            {{ flight.aircraft.airline.code + " " + flight.id + " " + flight.aircraft.type.name }}
          </q-item-label>
          <q-item-label caption>{{ flight.aircraft.airline.name }}</q-item-label>
        </q-item-section>

        <q-item-section class="items-end">
          <q-item-label>{{ getTime(flight.time_departure) }}</q-item-label>
          <q-item-label caption>{{ flight.flight_type.airport_departure.name }}</q-item-label>
          <q-item-label caption>{{ flight.flight_type.airport_departure.code }}</q-item-label>

        </q-item-section>

        <q-item-section class="col-1">
          <q-item-label caption>
            {{ getCostTime(flight.time_departure, flight.time_arrival) }}
          </q-item-label>
          <q-item-label>
            <q-img src="~assets/arrow4.png"  />
          </q-item-label>
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ getTime(flight.time_arrival) }}</q-item-label>
          <q-item-label caption>{{ flight.flight_type.airport_arrival.name }}</q-item-label>
          <q-item-label caption>{{ flight.flight_type.airport_arrival.code }}</q-item-label>

        </q-item-section>

        <q-item-section side>
          <q-chip :color="getStatus(flight.status, flight.time_departure).color" text-color="white" icon="alarm" >
            <q-item-label>{{ getStatus(flight.status, flight.time_departure).status }}</q-item-label>
          </q-chip>
        </q-item-section>

      </q-item>
    </q-list>
    <q-dialog v-model="card" >
      <q-card class="my-card" style="width: 450px;">
        <q-card-section>
          <q-input filled label="出发时间" class="q-my-md" v-model="time_departure">
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

          <q-input filled label="到达时间" class="q-my-md" v-model="time_arrival">
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
        <q-card-section align="right">
          <q-btn flat @click="card = false" color="primary" label="取消" class="q-mx-sm" />
          <q-btn v-close-popup color="primary" :label="cardStatus" @click="confirm" class="q-mx-sm" />
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { date, useQuasar } from 'quasar';
const $q = useQuasar()
import { onMounted, ref } from 'vue'
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
const getStatus = (status, time_departure) => {
  if (new Date() > new Date(time_departure)) {
    return {status: '已起飞', color: 'grey'}
  }

  if (status === 'cancel') {
    return {status: '已取消', color: 'red'}
  } else if (status === 'delay') {
    return {status: '延误', color: 'yellow-8'}
  }
  return {status: '准点', color: 'green'}
}

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

const clickModify = (id) => {
  modify_id = id

  cardStatus.value = "修改"

  const flight = flights.value.filter((flight) => flight.id === id)[0]

  if (getStatus(flight.status, flight.time_departure).status === '已起飞') {
    notify_error('已起飞的航班无法修改')
    return
  }
  card.value = true

  time_departure.value = date.formatDate(flight.time_departure, 'YYYY-MM-DD HH:mm')
  time_arrival.value = date.formatDate(flight.time_arrival, 'YYYY-MM-DD HH:mm')
  group.value = flight.status
}


const confirm = () => {
  const url = '/flights/id/' + modify_id
  const flight = flights.value.filter((flight) => flight.id === modify_id)[0]
  const data = {
    aircraft_id: flight.aircraft_id,
    flight_type_id: flight.flight_type_id,
    price0: flight.price0,
    price1: flight.price1,
    price2: flight.price2,

    time_departure: time_departure.value,
    time_arrival: time_arrival.value,
    status: group.value,
  }
  api.put(url, data).then((res) => {
    updateFlights()
    card.value = false
    notify_success('修改成功!')
  }).catch((err) => {
    console.log(err)
    notify_error('修改失败!')
  })
}

const flights = ref([])

const updateFlights = () => {
  const airport_code_departure = $userStore.admin_type.slice(8)
  const airport_code_arrival = $userStore.admin_type.slice(8)
  const url = '/flights/airport/'
  flights.value = []
  api.get(url, {
    params: {
      airport_code_departure: airport_code_departure,
    }
  }).then((res) => {
    const data = res.data
    for (let flight of data) {
      flight.aircraft.type.model = JSON.parse(flight.aircraft.type.model)
    }
    flights.value.push(...data)
    flights.value.sort((a, b) => {
      return new Date(a.time_departure) - new Date(b.time_departure)
    })
  })
  api.get(url, {
    params: {
      airport_code_arrival: airport_code_arrival,
    }
  }).then((res) => {
    const data = res.data
    for (let flight of data) {
      flight.aircraft.type.model = JSON.parse(flight.aircraft.type.model)
    }
    flights.value.push(...data)
    flights.value.sort((a, b) => {
      return new Date(a.time_departure) - new Date(b.time_departure)
    })
  })
}

const updateAll = () => {
  updateFlights()
}
onMounted(() => {
  updateAll()
})
setInterval(() => {
  updateAll()
}, 1000 * 60);


</script>
