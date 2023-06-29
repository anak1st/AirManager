<template>
  <q-page class="q-pa-lg">
    <h5 class="q-mt-none">User Main Page</h5>
    <q-list bordered>
      <q-item
        v-for="flight in flights"
        :key="flight.id"
        class="q-my-sm row"
        clickable
        v-ripple
      >
        <q-item-section class="col-1" avatar>
          <q-avatar color="primary" text-color="white">
            {{ flight.aircraft.airline.name[0] }}
          </q-avatar>
        </q-item-section>

        <q-item-section class="col-2">
          <q-item-label>{{ flight.aircraft.airline.name }}</q-item-label>
          <q-item-label caption>{{ flight.aircraft.airline.code }}</q-item-label>
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

        <q-item-section side>
          <q-icon name="chat_bubble" color="green" />
        </q-item-section>
      </q-item>
    </q-list>
  </q-page>
</template>

<script setup>
import { date } from 'quasar';
import { onMounted, ref } from 'vue'
import { api } from 'src/boot/axios';

const flights = ref([])

const updateFlights = () => {
  api.get('/flights').then((res) => {
    console.log(res.data)
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

  return cost
}

const updateAll = () => {
  updateFlights()
}
onMounted(() => {
  updateAll()
})
setInterval(() => {
  updateAll()
}, 1000*10);


</script>
