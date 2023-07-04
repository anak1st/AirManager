<template>
  <q-page>
    <q-list bordered>
      <q-item class="q-my-sm row">
        <q-item-section>
          <q-select filled v-model="airport_departure" :options="airports" label="出发" />
        </q-item-section>
        <q-item-section>
          <q-select filled v-model="airport_arrival" :options="airports" label="到达" />
        </q-item-section>
        <q-item-section style="max-width: 150px;">
          <q-btn label="展示所有航班" @click="showall = !showall" />
        </q-item-section>
      </q-item>
      <q-item
        v-for="flight in flights"
        :key="flight.id"
        class="q-my-sm row"
        clickable
        v-show="showall
             || getStatus(flight.status, flight.time_departure).status === '延误'
             || getStatus(flight.status, flight.time_departure).status === '准点'"
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
              起步价 {{ flight.price0 / 100 }}
            </q-chip>
          </q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-chip :color="getStatus(flight.status, flight.time_departure).color" text-color="white" icon="alarm" >
            <q-item-label>{{ getStatus(flight.status, flight.time_departure).status }}</q-item-label>
          </q-chip>
        </q-item-section>

        <q-item-section side>
          <q-btn color="red" label="购买" @click="bookFlights(flight.id)" />
        </q-item-section>
      </q-item>
    </q-list>
    <q-dialog v-model="bookFlightsCard" >
      <q-card class="my-card" style="width: 800px">
          <div class="q-my-md text-h6 text-center"> 购买 </div>
        <q-card-section class="column items-start">

          <q-chip icon="airline_seat_recline_extra" color="green-4">
            <div> 经济舱价格 {{ price[0] }}, 剩余 {{ seatTypes[0] }} </div>
          </q-chip>
          <q-chip icon="airline_seat_recline_extra" color="blue-4">
            <div> 商务舱价格 {{ price[1] }}, 剩余 {{ seatTypes[1] }} </div>
          </q-chip>
          <q-chip icon="airline_seat_recline_extra" color="yellow-4">
            <div> 头等舱价格 {{ price[2] }}, 剩余 {{ seatTypes[2] }} </div>
          </q-chip>


        </q-card-section>
        <q-card-section>
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
          <q-chip color="teal" text-color="white" icon="bookmark">
            <div> 你选择了 {{ selectSeat }} </div>
          </q-chip>
          <span class="text-subtitle1">
            钱包余额 <span class="text-red">{{ money / 100 }}</span>;
            目前积分 <span class="text-orange">{{ points / 100 }}</span>,
            VIP 等级为 <span class="text-orange">{{ getVip() }}</span>
          </span>
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

import { onMounted, ref, watch } from 'vue'
import { api } from 'src/boot/axios';
import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()

const notify_sucess = (message) => {
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

const showall = ref(false)
const flights = ref([])

const airport_departure = ref([])
const airport_arrival = ref([])
const updateFlights = () => {
  if (airport_departure.value.length === 0 || airport_arrival.value.length === 0) {
    const url = '/flights/'
    api.get(url).then((res) => {
      flights.value = res.data
      for (let flight of flights.value) {
        flight.aircraft.type.model = JSON.parse(flight.aircraft.type.model)
      }
      flights.value.sort((a, b) => {
        return a.time_departure > b.time_departure ? 1 : -1
      })
    })
    return
  }

  const airport_code_departure = airport_departure.value.code
  const airport_code_arrival = airport_arrival.value.code
  // console.log(airport_code_departure, airport_code_arrival)
  const url = '/flights/airport/'
  api.get(url, {
    params: {
      airport_code_departure: airport_code_departure,
      airport_code_arrival: airport_code_arrival,
    }
  }).then((res) => {
    flights.value = res.data
    for (let flight of flights.value) {
      flight.aircraft.type.model = JSON.parse(flight.aircraft.type.model)
    }
  })
}

watch([airport_departure, airport_arrival], () => {
  updateFlights()
})

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


const price = ref([])
const bookFlightsCard = ref(false)
const flight_id = ref('')
const bookFlights = async (id) => {
  flight_id.value = id

  const flight = flights.value.find((flight) => flight.id === id)

  const status = getStatus(flight.status, flight.time_departure)
  if (status.status === '已取消' || status.status === '已起飞') {
    notify_error('航班状态不允许购买')
    return
  }
  bookFlightsCard.value = true

  price.value[0] = flight.price0 / 100
  price.value[1] = flight.price1 / 100
  price.value[2] = flight.price2 / 100
  const model = flight.aircraft.type.model
  const books = await updateBooks()
  initList(model.seat, books)
}

const row = 100
let List = []
const itemsCount = ref(0)
const seatTypes = ref([])
const initList = (seat, books) => {
  List = []
  seatTypes.value = []
  seatTypes.value[0] = 0
  seatTypes.value[1] = 0
  seatTypes.value[2] = 0

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
        let colour = 'bg-green'
        if (seat[label].type === 1) {
          colour = 'bg-blue'
        }
        if (seat[label].type === 2) {
          colour = 'bg-yellow-8'
        }
        seatTypes.value[seat[label].type] += 1

        if (books.find((book) => book.seat === label)) {
          colour = 'bg-red'
          seatTypes.value[seat[label].type] -= 1
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

const money = ref(0)
const points = ref(0)
const updeteUserInfo = () => {
  const url = '/users/id/' + $userStore.id
  api.get(url).then((res) => {
    money.value = res.data.money
    points.value = res.data.points
  })
}
const getVip = () => {
  if (points.value / 100 >= 10000) {
    return 2
  }
  if (points.value / 100 >= 1000) {
    return 1
  }
  return 0
}

const buyFlights = () => {
  if (selectSeat.value === '') {
    notify_error('请选择座位')
    return
  }

  const flight = flights.value.find((flight) => flight.id === flight_id.value)
  const seat_type = flight.aircraft.type.model.seat[selectSeat.value].type

  let price = 0
  if (seat_type === 0) { price = flight.price0 }
  if (seat_type === 1) { price = flight.price1 }
  if (seat_type === 2) { price = flight.price2 }
  if (price === 0) {
    notify_error('价格错误')
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
    notify_sucess('购买成功')
    bookFlightsCard.value = false
  }).catch((err) => {
    notify_error('购买失败')
    console.log(err)
  })
}

const airports = ref([])

const updateAirports = () => {
  const url = '/airports'
  api.get(url).then((res) => {
    airports.value = res.data
    for (let airport of airports.value) {
      airport.label = airport.name + ' (' + airport.code + ')'
      airport.value = airport.code
    }
  })
}

const updateAll = () => {
  updeteUserInfo()
  updateFlights()
  updateAirports()
}
onMounted(() => {
  updateAll()
})
setInterval(() => {
  updateAll()
}, 1000 * 60);

</script>

<style lang="scss">

.items {
  width: 12px;
  height: 12px;
  background-color: red;
  margin: 1px;
}

</style>
