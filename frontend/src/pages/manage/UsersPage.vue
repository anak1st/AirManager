<template>
  <div class="row no-wrap shadow-1">
    <q-toolbar class="" :class="$q.dark.isActive ? 'bg-grey-9 text-white' : 'bg-grey-3'">
      <q-btn flat round dense icon="search" />
      <q-toolbar-title>
        <q-input
          filled
          dense
          v-model="searchThing"
        />
      </q-toolbar-title>
      <q-select
        filled
        dense
        v-model="searchWhat"
        :options="['用户名', '邮箱', '实名']"
        style="width: 100px;"
      />
    </q-toolbar>
    <q-space />
  </div>
  <q-page class="bg-grey-1 q-pa-md column">
    <div>
      <q-table
        flat bordered
        :rows="users"
        :columns="userColumns"
        row-key="id"
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
        <!-- <q-btn color="accent" icon="card_giftcard" label="添加" /> -->
        <q-btn color="accent" icon="create" label="删除" @click="deleteUser">
          : {{ getSelectedUser() }}
        </q-btn>
      </q-btn-group>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { api } from 'src/boot/axios';
import { useQuasar } from 'quasar';
const $q = useQuasar()
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

const searchWhat = ref('')
const searchThing = ref('')
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
  if (searchWhat.value === '' || searchThing.value == '') {
    api.get('/users/').then((res) => {
      users.value = res.data
    })
    return
  }
  if (searchWhat.value === '用户名') {
    api.get('/users/search/', {
      params: {
        username: searchThing.value
      }
    }).then((res) => {
      users.value = res.data
    })
    return
  }
  if (searchWhat.value === '邮箱') {
    api.get('/users/search/', {
      params: {
        email: searchThing.value
      }
    }).then((res) => {
      users.value = res.data
    })
    return
  }
  if (searchWhat.value === '实名') {
    api.get('/users/search/', {
      params: {
        fullname: searchThing.value
      }
    }).then((res) => {
      users.value = res.data
    })
    return
  }
}

watch([searchWhat, searchThing], () => {
  updateUsers()
})

const getSelectedUser = () => {
  if (userSelected.value.length === 0) {
    return 'null'
  }
  return userSelected.value[0].email
}

const deleteUser = () => {
  if (getSelectedUser() === 'null') {
    notify_error('请选择一个用户')
    return
  }

  $q.dialog({
    title: '删除用户',
    message: '确定删除用户 ' + getSelectedUser() + ' 吗？',
    ok: '确定',
    cancel: '取消',
    persistent: true
  }).onOk(() => {
    const id = userSelected.value[0].id
    api.delete('/users/id/' + id).then((res) => {
      notify_success('删除成功')
      updateUsers()
    }).catch((err) => {
      notify_error('删除失败')
      console.log(err)
    })
  })
}

const updateAll = () => {
  updateUsers()
}
onMounted(() => {
  updateAll()
})
// every 10s update
setInterval(() => {
  updateAll()
}, 1000 * 60)

</script>

<style lang="scss">

</style>
