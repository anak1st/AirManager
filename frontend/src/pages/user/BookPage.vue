<template>
  <q-page>
    <q-list bordered>
      <div
        class="column q-my-sm"
        v-for="book in books"
        :key="book.id"
      >
        <q-item
          class="row"
          clickable
          v-ripple
          @click="book.show = !book.show"
        >
          <q-item-section avatar>
            <q-avatar color="primary" text-color="white">
              <q-item-label>{{ book.flight.aircraft.airline.name[0] }}</q-item-label>
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label>
              {{ book.flight.aircraft.airline.code + " " + book.flight.id + " " + book.flight.aircraft.type.name }}
            </q-item-label>
            <q-item-label caption>{{ book.flight.aircraft.airline.name }}</q-item-label>
          </q-item-section>

          <q-item-section class="items-end">
            <q-item-label>{{ getTime(book.flight.time_departure) }}</q-item-label>
            <q-item-label caption>{{ book.flight.flight_type.airport_departure.name }}</q-item-label>
            <q-item-label caption>{{ book.flight.flight_type.airport_departure.code }}</q-item-label>

          </q-item-section>

          <q-item-section class="col-1">
            <q-item-label caption>
              {{ getCostTime(book.flight.time_departure, book.flight.time_arrival) }}
            </q-item-label>
            <q-item-label>
              <q-img src="~assets/arrow4.png"  />
            </q-item-label>
          </q-item-section>

          <q-item-section>
            <q-item-label>{{ getTime(book.flight.time_arrival) }}</q-item-label>
            <q-item-label caption>{{ book.flight.flight_type.airport_arrival.name }}</q-item-label>
            <q-item-label caption>{{ book.flight.flight_type.airport_arrival.code }}</q-item-label>
          </q-item-section>

          <q-item-section side>
            <q-chip :color="getStatus(book.flight.status, book.flight.time_departure).color" text-color="white" icon="alarm" >
              <q-item-label>{{ getStatus(book.flight.status, book.flight.time_departure).status }}</q-item-label>
            </q-chip>
          </q-item-section>

          <q-item-section class="col-1" side>
            <q-btn round color="red" icon="delete" @click="confirm(book.id)" />
          </q-item-section>
        </q-item>
        <q-item
          class="row"
          clickable
          v-ripple
          v-show="book.show"
        >
         <q-item-section side>
            <q-item-label>
              <q-chip icon="payment">
                已支付 {{ book.pay / 100 }} 元
              </q-chip>
            </q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>
              <q-chip icon="airline_seat_recline_extra">
                座位 {{ book.seat }}
              </q-chip>
            </q-item-label>
          </q-item-section>
        </q-item>
      </div>
      <q-item>
        <q-item-section side>
          <q-btn class="q-mx-lg" color="grey" icon="update" label="展示历史"
            @click="show_history = !show_history"
          />
        </q-item-section>
      </q-item>
      <div
        class="column q-my-sm"
        v-show="show_history"
        v-for="book in books_history"
        :key="book.id"
      >
        <q-item
          class="row"
          clickable
          v-ripple
          @click="book.show = !book.show"
        >
          <q-item-section avatar>
            <q-avatar color="primary" text-color="white">
              <q-item-label>{{ book.flight.aircraft.airline.name[0] }}</q-item-label>
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label>
              {{ book.flight.aircraft.airline.code + " " + book.flight.id + " " + book.flight.aircraft.type.name }}
            </q-item-label>
            <q-item-label caption>{{ book.flight.aircraft.airline.name }}</q-item-label>
          </q-item-section>

          <q-item-section class="items-end">
            <q-item-label>{{ getTime(book.flight.time_departure) }}</q-item-label>
            <q-item-label caption>{{ book.flight.flight_type.airport_departure.name }}</q-item-label>
            <q-item-label caption>{{ book.flight.flight_type.airport_departure.code }}</q-item-label>

          </q-item-section>

          <q-item-section class="col-1">
            <q-item-label caption>
              {{ getCostTime(book.flight.time_departure, book.flight.time_arrival) }}
            </q-item-label>
            <q-item-label>
              <q-img src="~assets/arrow4.png"  />
            </q-item-label>
          </q-item-section>

          <q-item-section>
            <q-item-label>{{ getTime(book.flight.time_arrival) }}</q-item-label>
            <q-item-label caption>{{ book.flight.flight_type.airport_arrival.name }}</q-item-label>
            <q-item-label caption>{{ book.flight.flight_type.airport_arrival.code }}</q-item-label>
          </q-item-section>

          <q-item-section side>
            <q-chip :color="getStatus(book.flight.status, book.flight.time_departure).color" text-color="white" icon="alarm" >
              <q-item-label>{{ getStatus(book.flight.status, book.flight.time_departure).status }}</q-item-label>
            </q-chip>
          </q-item-section>

          <q-item-section class="col-1" side>
            <q-btn round color="grey" icon="delete" />
          </q-item-section>
        </q-item>
        <q-item
          class="row"
          clickable
          v-ripple
          v-show="book.show"
        >
         <q-item-section side>
            <q-item-label>
              <q-chip icon="payment">
                 {{ book.pay > 0 ? "已支付 " + book.pay / 100 + " 元" : "已退款" }}
              </q-chip>
            </q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label>
              <q-chip icon="airline_seat_recline_extra">
                座位 {{ book.seat }}
              </q-chip>
            </q-item-label>
          </q-item-section>
        </q-item>
      </div>

    </q-list>
  </q-page>
</template>

<script setup>
import { date, useQuasar } from 'quasar';
const $q = useQuasar()
import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()
import { onMounted, ref } from 'vue';
import { api } from 'src/boot/axios';

const show_history = ref(true)

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

const books = ref([])
const showMore = ref([])
const updateBooks = () => {
  const url = '/books/user/' + $userStore.id
  return api.get(url).then((res) => {
    const backups = books.value
    books.value = res.data
    showMore.value = []
    // console.log(books.value)
    for (const book of books.value) {
      const backup = backups.find((backup) => backup.id == book.id)
      if (backup) {
        book.show = backup.show
      } else {
        book.show = false
      }
    }
    books.value.sort((a, b) => {
      return new Date(a.flight.time_departure) - new Date(b.flight.time_departure)
    })
  }).catch((err) => {
    console.log(err)
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

const confirm = (id) => {
  const book = books.value.find((book) => book.id === id)
  const status = book.flight.status
  const time_departure = book.flight.time_departure
  if (status !== 'cancel' && new Date() > new Date(time_departure)) {
    notify_error('该航班已起飞')
    return
  }


  $q.dialog({
    title: '删除订单',
    message: '确定删除订单吗？',
    ok: '确定',
    cancel: '取消',
    persistent: true,
  }).onOk(() => {
    const url = '/books/id/' + id
    api.delete(url).then((res) => {
      updateAll()
      notify_sucess('删除成功')
    }).catch((err) => {
      notify_error('删除失败')
      console.log(err)
    })
  })
}

const books_history = ref([])
const updateBooksHistory = () => {
  const url = '/books_history/user/' + $userStore.id
  return api.get(url).then((res) => {
    books_history.value = res.data
    showMore.value = []
    // console.log(books.value)
    books_history.value.sort((a, b) => {
      return new Date(a.flight.time_departure) - new Date(b.flight.time_departure)
    })
  }).catch((err) => {
    console.log(err)
  })
}

const updateAll = () => {
  updateBooks()
  updateBooksHistory()
}

onMounted(() => {
  updateAll()
})

setInterval(() => {
  updateAll()
}, 1000 * 60);

</script>
