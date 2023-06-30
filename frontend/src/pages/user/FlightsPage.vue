<template>
  <q-page>
    <q-list bordered>
      <q-item
        v-for="flight in flights"
        :key="flight.id"
        class="q-my-sm row"
        clickable

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
          <q-item-label>
            <q-chip color="red" text-color="white" icon="directions">
              起步价 {{ flight.price0 }}
            </q-chip>
          </q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-chip :color="flight.status === 'normal' ? 'green' : 'red'" text-color="white" icon="alarm" >
            <q-item-label>{{ getStatus(flight.status) }}</q-item-label>
          </q-chip>
        </q-item-section>

        <q-item-section side>
          <q-btn color="red" label="购买" @click="bookFlights(flight.id)" />
        </q-item-section>
      </q-item>
    </q-list>
    <q-dialog v-model="bookFlightsCard" >
      <q-card class="my-card" style="width: 800px">

        <q-card-section>
          <div class="q-my-md text-h6 text-center"> 购买 </div>
          <div> {{ itemsCount }} </div>
          <q-virtual-scroll
            :items="List"
            virtual-scroll-horizontal
            v-slot="{ item, index }"
          >
            <div
              :key="index"
              class="column"
            >
              <div class="text-center"> {{ item.label }} </div>
              <q-btn
                v-for="col of item"
                :key="col.label"
                style="margin: 2px;"
                :class="col.color"
                @click="selectSeat = col.label"
              >
                {{ col.label.slice(2) }}
              </q-btn>
            </div>
          </q-virtual-scroll>
        </q-card-section>
        <q-card-section>
          <div>你选择了 {{ selectSeat }}</div>
        </q-card-section>
        <q-card-section align="right">
          <q-btn class="q-mx-sm text-black" label="取消"  @click="bookFlightsCard = false" />
          <q-btn class="q-mx-sm" label="购买" color="primary" @click="buyFlights" />
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

const flights = ref([])

const updateFlights = () => {
  const url = '/flights/'
  api.get(url).then((res) => {
    flights.value = res.data
    for (let flight of flights.value) {
      flight.aircraft.type.model = JSON.parse(flight.aircraft.type.model)
      // console.log(flight)
    }
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

const bookFlightsCard = ref(false)
const flight_id = ref('')
const bookFlights = async (id) => {
  flight_id.value = id
  bookFlightsCard.value = true
  const flight = flights.value.find((flight) => flight.id === id)
  const model = flight.aircraft.type.model
  const books = await updateBooks()
  initList(model.seat, books)
}

const row = 100
let List = []
const itemsCount = ref(0)

const initList = (seat, books) => {
  // console.log(seat)
  List = []
  itemsCount.value = 0
  for (let i = 1; i <= row; i++) {
    let listRow = []
    listRow.label = i
    for (let j of ['A', 'B', 'C', 'D', 'E', 'F']) {
      let label = i + j
      if (label.length < 3) {
        label = '0' + label
      }

      if (seat.hasOwnProperty(label)) {
        // console.log('has')
        let colour = 'bg-green'
        if (seat[label].type === 1) {
          colour = 'bg-blue'
        }
        if (books.find((book) => book.seat === label)) {
          colour = 'bg-red'
        }

        listRow.push({
          label: label,
          color: colour
        })
        itemsCount.value += 1
        continue
      }
    }
    if (listRow.length > 0) {
      List.push(listRow)
    }
  }
}

const selectSeat = ref('')
const updateBooks = async () => {
  const url = '/books/flight/' + flight_id.value
  let books = []
  await api.get(url).then((res) => {
    books = res.data
  }).catch((err) => {
    console.log(err)
  })
  return books
}

const buyFlights = () => {
  if (selectSeat.value === '') {
    $q.notify({
      message: '请选择座位',
      color: 'red',
      icon: 'close'
    })
    return
  }

  const flight = flights.value.find((flight) => flight.id === flight_id.value)
  const seat_type = flight.aircraft.type.model.seat[selectSeat.value].type

  let price = 0
  if (seat_type === 0) {
    price = flight.price0
  }
  if (seat_type === 1) {
    price = flight.price1
  }
  if (seat_type === 2) {
    price = flight.price2
  }
  if (price === 0) {
    $q.notify({
      message: '价格错误',
      color: 'red',
      icon: 'close'
    })
    return
  }

  const url = '/books/'
  const data = {
    flight_id: flight_id.value,
    user_id: $userStore.id,
    seat: selectSeat.value,
    status: 'normal',
    pay: price
  }

  api.post(url, data).then((res) => {
    $q.notify({
      message: '购买成功',
      color: 'green',
      icon: 'check'
    })
    bookFlightsCard.value = false
  }).catch((err) => {
    $q.notify({
      message: '购买失败',
      color: 'red',
      icon: 'close'
    })
    console.log(err)
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
}, 1000 * 10);

</script>

<style lang="scss">

.items {
  width: 12px;
  height: 12px;
  background-color: red;
  margin: 1px;
}

</style>
