<template>
  <div class="row no-wrap shadow-1">
    <q-toolbar class="col-9" :class="$q.dark.isActive ? 'bg-grey-9 text-white' : 'bg-grey-3'">
      <q-btn flat round dense icon="search" />
      <q-toolbar-title>Search</q-toolbar-title>

    </q-toolbar>
    <q-space />
    <q-toolbar class="col-3 bg-primary text-white">
      <q-space />
      <q-btn flat round dense icon="bluetooth" class="q-mr-sm" />
      <q-btn flat round dense icon="more_vert" />
    </q-toolbar>
  </div>
  <q-page class="bg-grey-1 column">
    <div>
      <q-table
        flat
        :rows="users"
        :columns="userColumns"
        row-key="name"
        selection="single"
        v-model:selected="userSelected"
        rows-per-page-label="每页行数"
        :selected-rows-label="(numberOfRows) => {
          return '选中了第' + String(numberOfRows) + '行'
        }"
        :pagination-label="(firstRowIndex, endRowIndex, totalRowsNumber) => {
          return `${firstRowIndex} - ${endRowIndex} / ${totalRowsNumber}`
        }"
      />
      <q-btn-group class="q-my-md">
        <q-btn color="accent" icon="card_giftcard" label="添加" />
        <q-btn color="accent" icon="create" label="删除">
          : {{ "无" }}
        </q-btn>
      </q-btn-group>
    </div>
    <q-dialog v-model="modifyUserCard" >
      <q-card class="my-card" style="width: 400px;">
        <q-img src="~assets/A380.jpg" style="height: 150px;" />

        <q-card-section>
          <div class="q-my-md text-h4 text-center"> 添加机场管理员 </div>

          <q-input filled class="q-ma-md" v-model="modifyUserCard" label="密码"   />
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
import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()

const users = ref([])
const userSelected = ref([])
const userColumns = [
  {
    name: 'id',
    required: true,
    label: 'ID',
    align: 'left',
    field: 'id',
    sortable: true
  },
  {
    name: 'email',
    align: 'left',
    label: '邮箱',
    field: 'email',
    sortable: true
  },
  {
    name: 'phone',
    align: 'left',
    label: '手机号',
    field: 'phone',
    sortable: true
  },
  {
    name: 'username',
    align: 'left',
    label: '用户名',
    field: 'username',
    sortable: true
  },
  {
    name: 'fullname',
    align: 'left',
    label: '姓名',
    field: 'fullname',
    sortable: true
  },
]

const updateUsers = () => {
  api.get('/users/').then((res) => {
    users.value = res.data
    console.log(res.data)
  })
}

const getSelectedUser = () => {
  if (userSelected.value.length === 0) {
    return null
  }
  return userSelected.value[0]
}

const modifyUserCard = ref(false)

const updateAll = () => {
  updateUsers()
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
