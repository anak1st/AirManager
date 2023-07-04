<template>
  <q-page>
    <q-list bordered>
      <q-item class="q-my-sm row">
        <q-item-section>
          <q-item-label class="text-h6">销售总额: 共售机票 {{ sale_num }} 张, 总销售额 {{ sale }} 元.</q-item-label>
        </q-item-section>
      </q-item>
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

        <q-item-section side>
          <q-item-label>已售 {{ flight.sale_num }} 张</q-item-label>
          <q-item-label caption> {{ flight.sale / 100 }} 元</q-item-label>
        </q-item-section>

      </q-item>
    </q-list>
    <q-dialog v-model="card" >
      <q-card class="my-card" style="width: 450px;">
        <q-stepper
          v-model="step"
          ref="stepper"
          alternative-labels
          color="primary"
          animated
        >
          <q-step
            :name="1"
            title="航班信息"
            icon="settings"
            :done="step > 1"
          >
            <q-card-section>

              <q-select filled class="q-md-md" v-model="aircraft_id" :options="aircrafts" label="飞机代码" />

              <q-select filled class="q-my-md" v-model="flight_type_id" :options="flight_types" label="航班路线" />

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
            <q-stepper-navigation align="right">
              <q-btn @click="goto2" color="primary" label="继续" />
            </q-stepper-navigation>
          </q-step>

          <q-step
            :name="2"
            title="价格信息"
            icon="create_new_folder"
            :done="step > 2"
          >
            <q-input filled type="number" v-model="price0" label="经济舱价格" class="q-my-md" />
            <q-input filled type="number" v-model="price1" label="商务舱价格" class="q-my-md" />
            <q-input filled type="number" v-model="price2" label="头等舱价格" class="q-my-md" />
            <q-stepper-navigation align="right">
              <q-btn flat @click="step = 1" color="primary" label="返回" class="q-mx-sm" />
              <q-btn @click="goto3" color="primary" label="继续" class="q-mx-sm"/>
            </q-stepper-navigation>
          </q-step>

          <q-step
            :name="3"
            title="完成"
            icon="add_comment"
          >
            确认{{ cardStatus }}航班吗？
            <q-stepper-navigation align="right">
              <q-btn flat @click="step = 2" color="primary" label="返回" class="q-mx-sm" />
              <q-btn v-close-popup color="primary" :label="cardStatus" @click="confirm" class="q-mx-sm" />
            </q-stepper-navigation>
          </q-step>
        </q-stepper>
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

const step = ref(1)

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
    updateFlightsSale()
  })
}

const updateFlightsSale = () => {
  for (let flight of flights.value) {
    api.get('/books/num/flight_id/' + flight.id).then((res) => {
      flight.sale_num = res.data
    })
    api.get('/books/pay/flight_id/' + flight.id).then((res) => {
      flight.sale = res.data
    })
  }
}

const sale_num = ref(0)
const sale = ref(0)
const updateSale = () => {
  const airline_code = $userStore.admin_type.slice(8)
  api.get('/books/num/airline_code/' + airline_code).then((res) => {
    sale_num.value = res.data
  })
  api.get('/books/pay/airline_code/' + airline_code).then((res) => {
    sale.value = res.data
  }).catch((err) => {
    console.log(err)
  })
}

let aircrafts = []
const updateAircrafts = () => {
  const url = '/aircrafts/airline_code/' + $userStore.admin_type.slice(8)
  api.get(url).then((res) => {
    aircrafts = res.data
    for (let aircraft of aircrafts) {
      aircraft.label = ' (' + aircraft.id + ') ' + aircraft.type.name
      aircraft.value = aircraft.id
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
const getStatus = (status, time_departure) => {
  if (status === 'cancel') {
    return {status: '已取消', color: 'red'}
  }
  if (new Date() > new Date(time_departure)) {
    return {status: '已起飞', color: 'grey'}
  }
  if (status === 'delay') {
    return {status: '延误', color: 'yellow-8'}
  }
  return {status: '准点', color: 'green'}
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

const goto2 = () => {
  if (aircraft_id.value === '') {
    notify_error('请选择飞机')
    return
  }
  if (flight_type_id.value === '') {
    notify_error('请选择航班类型')
    return
  }
  if (time_departure.value === '') {
    notify_error('请选择起飞时间')
    return
  }
  if (time_arrival.value === '') {
    notify_error('请选择到达时间')
    return
  }
  if (time_departure.value >= time_arrival.value) {
    notify_error('到达时间必须晚于起飞时间')
    return
  }
  if (new Date(time_departure.value) < new Date()) {
    notify_error('起飞时间必须晚于当前时间')
    return
  }
  if (group.value === '') {
    notify_error('请选择航班状态')
    return
  }

  step.value = 2
}

const price0 = ref(0)
const price1 = ref(0)
const price2 = ref(0)

const goto3 = () => {
  if (parseInt(price0.value) > parseInt(price1.value)) {
    notify_error('经济舱价格必须小于或等于商务舱价格')
    return
  }
  if (parseInt(price1.value) > parseInt(price2.value)) {
    notify_error('商务舱价格必须小于或等于头等舱价格')
    return
  }
  step.value = 3
}

const clickAdd = () => {
  card.value = true
  cardStatus.value = "添加"
}
const clickModify = (id) => {
  modify_id = id
  card.value = true
  cardStatus.value = "修改"

  const flight = flights.value.filter((flight) => flight.id === id)[0]
  const aircraft = aircrafts.filter((aircraft) => aircraft.id === flight.aircraft_id)[0]
  const flight_type = flight_types.filter((flight_type) => flight_type.id === flight.flight_type_id)[0]

  aircraft_id.value = aircraft
  flight_type_id.value = flight_type
  time_departure.value = date.formatDate(flight.time_departure, 'YYYY-MM-DD HH:mm')
  time_arrival.value = date.formatDate(flight.time_arrival, 'YYYY-MM-DD HH:mm')
  group.value = flight.status
  price0.value = flight.price0 / 100
  price1.value = flight.price1 / 100
  price2.value = flight.price2 / 100
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
    aircraft_id: aircraft_id.value.id,
    flight_type_id: flight_type_id.value.id,
    time_departure: time_departure.value,
    time_arrival: time_arrival.value,
    status: group.value,
    price0: price0.value * 100,
    price1: price1.value * 100,
    price2: price2.value * 100
  }
  api.post(url, data).then((res) => {
    updateFlights()
    card.value = false
    notify_success('添加成功')
  }).catch((err) => {
    console.log(err)
    notify_error('添加失败')
  })
}

const confirmModify = () => {
  const url = '/flights/id/' + modify_id
  const data = {
    aircraft_id: aircraft_id.value.id,
    flight_type_id: flight_type_id.value.id,
    time_departure: time_departure.value,
    time_arrival: time_arrival.value,
    status: group.value,
    price0: price0.value * 100,
    price1: price1.value * 100,
    price2: price2.value * 100
  }
  console.log(data)
  api.put(url, data).then((res) => {
    updateAircrafts()
    updateFlights()
    card.value = false
    notify_success('修改成功')
  }).catch((err) => {
    console.log(err)
    notify_error('修改失败')
  })
}

const updateAll = () => {
  updateAircrafts()
  updateFlights()
  updateFlightTypes()
  updateSale()
}
onMounted(() => {
  updateAll()
})
setInterval(() => {
  updateAll()
}, 1000 * 60);


</script>
