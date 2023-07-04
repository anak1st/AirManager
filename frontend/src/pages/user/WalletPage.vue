<template>
  <q-page>
    <div class="q-my-md text-h4 text-center"> 钱包余额 {{ money / 100 }} 元 </div>
    <div class="q-my-md text-h4 text-center"> 积分 {{ points / 100 }} 点 </div>
    <div class="q-my-md text-h6 text-center"> 选择下面的套餐进行充值 </div>
    <div class="q-pa-md row items-start q-gutter-md">
      <q-card flat bordered class="my-card" v-for="gitcard of giftCards" :key="gitcard">
        <q-card-section>
          <div class="text-h6"> 方案 {{ gitcard.label }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div>
            充值 {{ gitcard.prise }} 元
            <q-chip dense color="orange" text-color="white" icon="star">
              返利 {{ gitcard.moneyadd }} 元
            </q-chip>
          </div>
          <div> 获得 {{ gitcard.prise + gitcard.moneyadd }} 元 </div>

        </q-card-section>

        <q-separator inset />

        <q-card-section>
          <q-btn
            color="primary"
            icon="local_grocery_store"
            label="充值"
            @click="chargeConfirm(gitcard.label)"
          />
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { api } from 'src/boot/axios';
import { useUserStore } from 'src/stores/user';
const $userStore = useUserStore()
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

const points = ref(0)
const money = ref(0)

const giftCards = [
  {
    label: 0,
    prise: -99999999,
    moneyadd: 0,
  },
  {
    label: 1,
    prise: 32,
    moneyadd: 4,
  },
  {
    label: 2,
    prise: 64,
    moneyadd: 10,
  },
  {
    label: 3,
    prise: 128,
    moneyadd: 25,
  },
  {
    label: 4,
    prise: 328,
    moneyadd: 64,
  },
  {
    label: 5,
    prise: 648,
    moneyadd: 180,
  }
]

const updateMoney = () => {
  const url = '/users/id/' + $userStore.id
  api.get(url).then((res) => {
    money.value = res.data.money
    points.value = res.data.points
  })
}

const chargeConfirm = (plan) => {
  $q.dialog({
    title: '充值',
    message: '确认充值吗?',
    ok: '确认',
    cancel: '取消',
    persistent: true
  }).onOk(() => {
    const url = '/users/id/' + $userStore.id + '/plan/' + plan
    api.get(url).then((res) => {
      notify_sucess('充值成功')
      updateMoney()
    }).catch((err) => {
      console.log(err)
      notify_error('充值失败')
    })
  })
}

const updateAll = () => {
  updateMoney()
}
onMounted(() => {
  updateAll()
})
setInterval(() => {
  updateAll()
}, 1000 * 5);

</script>

<style lang="sass" scoped>
.my-card
  width: 100%
  max-width: 250px
</style>
