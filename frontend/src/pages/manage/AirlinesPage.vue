<template>
  <q-page class="bg-grey-1 column">
    <q-tabs
      v-model="airlineTab"
      class="bg-grey-1 text-black"
      align="justify"
      narrow-indicator
    >
      <q-tab name="airlines" label="航空公司" />
      <q-tab name="airlineAdmins" label="航空公司管理员账号" />
    </q-tabs>

    <q-separator />

    <q-tab-panels
      v-model="airlineTab"
      dense
    >
      <q-tab-panel name="airlines">
        <q-table
          flat bordered
          :rows="airlines"
          :columns="airlineColumns"
          row-key="name"
          selection="single"
          v-model:selected="airlineSelected"
          separator="cell"
          rows-per-page-label="每页行数"
          :selected-rows-label="(numberOfRows) => {
            return '选中了第' + String(numberOfRows) + '行'
          }"
          :pagination-label="(firstRowIndex, endRowIndex, totalRowsNumber) => {
            return `${firstRowIndex} - ${endRowIndex} / ${totalRowsNumber}`
          }"
        />
        <q-btn-group class="q-ma-md">
          <q-btn color="accent" icon="card_giftcard" label="添加" />
          <q-btn color="accent" icon="create" label="删除">
            机场: {{ airlineSelected.length > 0 ? airlineSelected[0].name : "无" }}
          </q-btn>
        </q-btn-group>
      </q-tab-panel>

      <q-tab-panel name="airlineAdmins">
        <q-table
          flat bordered
          :rows="airlineAdmins"
          :columns="airlineAdminColumns"
          row-key="email"
          selection="single"
          v-model:selected="airlineAdminSelected"
          separator="cell"
        />
        <q-btn-group class="q-ma-md">
          <q-btn
            color="accent"
            icon="card_giftcard"
            label="添加"
            @click="addAdminCard = true"
          />
          <q-btn
            color="accent"
            icon="create"
            @click="deleteAdmin"
            label="删除"
          >
            管理员: {{ airlineAdminSelected.length > 0 ? airlineAdminSelected[0].email : "无" }}
          </q-btn>
        </q-btn-group>
      </q-tab-panel>
    </q-tab-panels>
    <q-dialog v-model="addAdminCard" >
      <q-card class="my-card" style="width: 400px;">
        <q-img src="~assets/A380.jpg" style="height: 150px;" />

        <q-card-section>
          <div class="q-my-md text-h4 text-center"> 添加航空公司管理员 </div>

          <q-select filled class="q-ma-md" v-model="addAdminName" :options="options" label="航空公司"  />
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

const airlines = ref([])
const airlineTab = ref('airlines')
const airlineSelected = ref([])
const airlineColumns = [
  {
    name: 'code',
    required: true,
    label: '代码',
    align: 'left',
    field: 'code',
    sortable: true
  },
  { name: 'name', align: 'left', label: '名字', field: 'name', sortable: true },
  { name: 'country', align: 'left', label: '国家/地区', field: 'country', sortable: true },
]

const options = ref([])
const updateOptions = () => {
  const tmp = []
  for (const it of airlines.value) {
    tmp.push(it.name)
  }
  options.value = tmp
}
const updateAirlines = () => {
  api.get('/airlines/').then((res) => {
    airlines.value = res.data
    updateOptions()
  })
}

const airlineAdmins = ref([])
const airlineAdminSelected = ref([])
const airlineAdminColumns = [
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

const updateAirlineAdmins = () => {
  api.get('/admins/airlines/').then((res) => {
    airlineAdmins.value = res.data
    updateOptions()
  })
}

const addAdminCard = ref(false)
const addAdminName = ref('')
const addAdminEmail = ref('')
const addAdminPassword = ref('')
const addAdmin = () => {
  if (addAdminName.value === '' || addAdminEmail.value === '' || addAdminPassword.value === '') {
    notify_error('请填写完整信息')
    return
  }

  const code = airlines.value.find((it) => it.name === addAdminName.value).code
  const admin_type = 'Airline ' + code
  console.log(admin_type)
  api.post('/admins/', {
    username: addAdminName.value,
    admin_type: admin_type,
    email: addAdminEmail.value,
    password: addAdminPassword.value,
  }).then((res) => {
    notify_sucess('添加成功')
    updateAirlineAdmins()
    addAdminName.value = ''
    addAdminEmail.value = ''
    addAdminPassword.value = ''
  }).catch((err) => {
    notify_error('添加失败')
    console.log(err)
  })
}


const deleteAdmin = () => {
  if (airlineAdminSelected.value.length === 0) {
    notify_error('请选择一个管理员')
    return
  }
  const id = airlineAdminSelected.value[0].id
  $q.dialog({
    title: '确认删除',
    message: '真的要删除管理员吗?',
    cancel: "取消",
    ok : "确认",
    persistent: true
  }).onOk(() => {
    api.delete('/admins/id/' + id + '/').then((res) => {
      notify_sucess('删除成功')
      updateAirlineAdmins()
      airlineAdminSelected.value = []
    }).catch((err) => {
      notify_error('删除失败')
      console.log(err)
    })
  })
}


const updateAll = () => {
  updateAirlines()
  updateAirlineAdmins()
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
