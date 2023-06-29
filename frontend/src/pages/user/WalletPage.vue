<template>
  <q-page>
    <div class="q-my-md text-h4 text-center"> 钱包余额 {{ money }} Fly币 </div>
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
          <div>获得 {{ gitcard.prise + gitcard.moneyadd }} Fly币 </div>

        </q-card-section>

        <q-separator inset />

        <q-card-section>
          <q-btn
            color="primary"
            icon="local_grocery_store"
            label="充值"
            @click="chargeConfirm(gitcard.prise + gitcard.moneyadd)"
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

const money = ref(0)

const giftCards = [
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
  })
}

const chargeConfirm = (moneyChange) => {
  $q.dialog({
    title: '充值',
    message: '确认充值吗?',
    ok: '确认',
    cancel: '取消',
    persistent: true
  }).onOk(() => {
    const url = '/users/id/' + $userStore.id
    api.get(url).then((res) => {
      const resdata = res.data
      resdata.money += moneyChange
      api.put(url, resdata).then((res) => {
        $q.notify({
          message: '充值成功',
          color: 'positive',
          icon: 'check',
          position: 'top'
        })
        updateMoney()
      }).catch((err) => {
        console.log(err)
        $q.notify({
          message: '充值失败',
          color: 'negative',
          icon: 'warning',
          position: 'top'
        })
      })
    }).catch((err) => {
      console.log(err)
      $q.notify({
        message: '用户信息获取失败',
        color: 'negative',
        icon: 'warning',
        position: 'top'
      })
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
