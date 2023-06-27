<template>
  <q-page class="bg-grey-1 column">
    <q-tabs
      v-model="airportTab"
      class="bg-grey-1 text-black"
      align="justify"
      narrow-indicator
    >
      <q-tab name="airports" label="机场" />
      <q-tab name="airportAdmins" label="机场管理员账号" />
    </q-tabs>

    <q-separator />

    <q-tab-panels
      v-model="airportTab"
      dense
    >
      <q-tab-panel name="airports">
        <q-table
          flat bordered
          :rows="airports"
          :columns="airportColumns"
          row-key="name"
          selection="single"
          v-model:selected="airportSelected"
        />
        <q-btn-group class="q-ma-md">
          <q-btn color="accent" icon="card_giftcard" label="添加" />
          <q-btn color="accent" icon="create" >
            删除: {{ airportSelected.length > 0 ? airportSelected[0].name : "无" }}
          </q-btn>
        </q-btn-group>
      </q-tab-panel>

      <q-tab-panel name="airportAdmins">
        <q-table
          flat bordered
          :rows="airportAdmins"
          :columns="airportAdminColumns"
          row-key="email"
          selection="single"
          v-model:selected="airportAdminSelected"
        />
        <q-btn-group class="q-ma-md">
          <q-btn
            color="accent"
            icon="card_giftcard"
            label="添加"
            @click="addAdminCard = true"
          />
          <q-btn color="accent" icon="create" @click="deleteAdmin" >
            删除管理员: {{ airportAdminSelected.length > 0 ? airportAdminSelected[0].email : "无" }}
          </q-btn>
        </q-btn-group>
      </q-tab-panel>
    </q-tab-panels>
    <q-dialog v-model="addAdminCard" >
      <q-card class="my-card" style="width: 400px;">
        <q-img src="~assets/A380.jpg" style="height: 200px;" />

        <q-card-section>
          <div class="q-my-md text-h4 text-center"> 添加机场管理员 </div>

          <q-select filled class="q-ma-md" v-model="addAdminName" :options="options" label="机场"  />
          <q-input filled class="q-ma-md" v-model="addAdminEmail" label="Email" />
          <q-input filled class="q-ma-md" v-model="addAdminPassword" label="密码" />

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


const airports = ref([])
const airportTab = ref('airports')
const airportSelected = ref([])
const airportColumns = [
  {
    name: 'code',
    required: true,
    label: '代码',
    align: 'left',
    field: 'code',
    sortable: true
  },
  { name: 'name', align: 'left', label: '名字', field: 'name', sortable: true },
  { name: 'country', align: 'left', label: '国家', field: 'country', sortable: true },
  { name: 'city', align: 'left', label: '城市', field: 'city', sortable: true },
]

const options = ref([])
const updateOptions = () => {
  const tmp = []
  for (const it of airports.value) {
    tmp.push(it.name)
  }
  options.value = tmp
}
const updateAirports = () => {
  api.get('/airports/').then((res) => {
    airports.value = res.data
    updateOptions()
  })
}

const airportAdmins = ref([])
const airportAdminSelected = ref([])
const airportAdminColumns = [
  {
    name: 'email',
    required: true,
    label: '邮箱',
    align: 'left',
    field: 'email',
    sortable: true
  },
  { name: 'username', align: 'left', label: '用户名', field: 'username', sortable: true },
  { name: 'admin_type', align: 'left', label: '权限', field: 'admin_type', sortable: true },
]

const updateAirportAdmins = () => {
  api.get('/admins/airpots/').then((res) => {
    airportAdmins.value = res.data
    updateOptions()
  })
}

const addAdminCard = ref(false)
const addAdminName = ref('')
const addAdminEmail = ref('')
const addAdminPassword = ref('')
const addAdmin = () => {
  if (addAdminName.value === '' || addAdminEmail.value === '' || addAdminPassword.value === '') {
    $q.notify({
      color: 'negative',
      message: '请填写完整信息',
      icon: 'report_problem',
    })
    return
  }

  const code = airports.value.find((it) => it.name === addAdminName.value).code
  const admin_type = 'Airport ' + code
  console.log(admin_type)
  api.post('/admins/', {
    username: addAdminName.value,
    admin_type: admin_type,
    email: addAdminEmail.value,
    password: addAdminPassword.value,
  }).then((res) => {
    $q.notify({
      color: 'positive',
      message: '添加成功',
      icon: 'check',
    })
    updateAirportAdmins()
    addAdminName.value = ''
    addAdminEmail.value = ''
    addAdminPassword.value = ''
  }).catch((err) => {
    $q.notify({
      color: 'negative',
      message: '添加失败',
      icon: 'report_problem',
    })
    console.log(err)
  })
}


const deleteAdmin = () => {
  if (airportAdminSelected.value.length === 0) {
    $q.notify({
      color: 'negative',
      message: '请选择一个管理员',
      icon: 'report_problem',
    })
    return
  }
  const id = airportAdminSelected.value[0].id
  $q.dialog({
    title: '确认删除',
    message: '真的要删除管理员吗?',
    cancel: "取消",
    ok : "确认",
    persistent: true
  }).onOk(() => {
    api.delete('/admins/id/' + id + '/').then((res) => {
      $q.notify({
        color: 'positive',
        message: '删除成功',
        icon: 'check',
      })
      updateAirportAdmins()
      airportAdminSelected.value = []
    }).catch((err) => {
      $q.notify({
        color: 'negative',
        message: '删除失败',
        icon: 'report_problem',
      })
      console.log(err)
    })
  })
}


const updateAll = () => {
  updateAirports()
  updateAirportAdmins()
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
