<template>
  <q-page >
    <q-list bordered>
      <q-item
        v-for="aircraft in aircrafts"
        :key="aircraft.id"
        class="q-my-sm row"
        clickable
        v-ripple
      >
        <q-item-section>
          <q-item-label>{{ aircraft.airline_code + " " + aircraft.id }}</q-item-label>
          <q-item-label caption>{{ aircraft.type_code }}</q-item-label>
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ aircraft.type.name }}</q-item-label>
        </q-item-section>

        <q-item-section>
          <q-item-label> 经济舱座位数量:{{ aircraft.type.model.seat_count0 }}</q-item-label>
        </q-item-section>

        <q-item-section>
          <q-item-label> 商务舱座位数量:{{ aircraft.type.model.seat_count1 }}</q-item-label>
        </q-item-section>

        <q-item-section>
          <q-item-label> 头等舱座位数量:{{ aircraft.type.model.seat_count2 }}</q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-item-label>
            <q-btn round color="red" icon="delete" @click="confirm(aircraft.id)" />
          </q-item-label>
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
          <div class="q-my-md text-h5 text-center"> 添加飞机类型! </div>

          <q-select
            filled
            class="q-ma-md"
            v-model="aircraft_type"
            :options="aircraft_types"
            label="飞机类型" />
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn v-close-popup color="primary" label="取消" />
          <q-btn v-close-popup color="primary" label="添加" @click="addAircraft" />
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

const aircrafts = ref([])
const updateAircrafts = () => {
  const url = '/aircrafts/airline_code/' + $userStore.admin_type.slice(8)
  api.get(url).then((res) => {
    aircrafts.value = res.data
    for (let aircraft of aircrafts.value) {
      aircraft.type.model = JSON.parse(aircraft.type.model)
      aircraft.type.model.seat_count0 = 0
      aircraft.type.model.seat_count1 = 0
      aircraft.type.model.seat_count2 = 0
      for (let key in aircraft.type.model.seat) {
        const seat = aircraft.type.model.seat[key]
        if (seat.type === 0) {
          aircraft.type.model.seat_count0 += 1
        } else if (seat.type === 1) {
          aircraft.type.model.seat_count1 += 1
        } else if (seat.type === 2) {
          aircraft.type.model.seat_count2 += 1
        }
      }
    }
  })
}

const cardAdd = ref(false)
let aircraft_types = []
const aircraft_type = ref([])

const updateAircraftTypes = () => {
  api.get('/aircraft_types').then((res) => {
    aircraft_types = res.data
    for (let aircraft_type of aircraft_types) {
      aircraft_type.label = ' (' + aircraft_type.code + ') ' + aircraft_type.name
      aircraft_type.value = aircraft_type.code
    }
  })
}

const addAircraft = () => {
  const airline_code = $userStore.admin_type.slice(8)
  api.post('/aircrafts', {
    airline_code: airline_code,
    type_code: aircraft_type.value.code,
  }).then((res) => {
    notify_sucess('添加成功!')
    updateAircrafts()
  }).catch((err) => {
    notify_error('添加失败!')
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
    api.delete('/aircrafts/id/' + id).then((res) => {
      notify_sucess('删除成功!')
      updateAircrafts()
    }).catch((err) => {
      console.log(err)
      notify_error('删除失败!')
    })
  })
}

const updateAll = () => {
  updateAircrafts()
  updateAircraftTypes()
}
onMounted(() => {
  updateAll()
})
setInterval(() => {
  updateAll()
}, 1000 * 10);


</script>
