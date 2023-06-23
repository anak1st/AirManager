<template>
  <q-page class="bg-grey-3 column">
    <q-list
      class="bg-white"
      separator
      bordered
    >
      <q-item
        v-for="task in tasks"
        :key="task.id"
        clickable
        @click="finishTask(task.id)"
        :class="{ 'bg-green-1' : task.is_done }"
        v-ripple
      >
        <q-item-section avatar>
          <q-checkbox
            v-model="task.done"
            class="no-pointer-events"
            val="teal"
            color="primary" />
        </q-item-section>
        <q-item-section>
          <q-item-label
            :class="{ 'done' : task.is_done }"
          >
            {{ task.title }}
          </q-item-label>
          <q-item-label caption lines="1">{{ task.description }}</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-item-label caption lines="1">{{ goodTime(task.deadline) }}</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-btn
            @click.stop="deleteTask(task.id)"
            flat
            round
            dense
            color="red"
            icon="delete" />
        </q-item-section>
      </q-item>
    </q-list>
    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn
        fab
        icon="add"
        color="accent"
        @click="card = true"
      />
    </q-page-sticky>
    <q-dialog v-model="card" >
      <q-card class="my-card" style="width: 400px;">
        <q-img src="~assets/GawrGura.png" />

        <q-card-section>
          <div class="q-my-md text-h4 text-center"> 添加一个任务吧! </div>

          <q-input
            filled
            class="q-my-sm"
            v-model="taskName"
            label="任务标题"
            hint=""
            lazy-rules
            :rules="[ val => val && val.length > 0 || '请输入任务标题']"
          />

          <q-input
            filled
            class="q-my-sm"
            v-model="taskDescription"
            label="任务简介"
            hint="请描述"
          />

          <q-input
            filled
            class="q-my-sm"
            v-model="taskDeadline"
            label="任务截止日期"
            mask="date"
            lazy-rules
            :rules="['date']">
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy cover :breakpoint="600">
                  <q-date v-model="taskDeadline" />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>

        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn v-close-popup color="primary" label="取消" />
          <q-btn v-close-popup color="primary" label="添加" @click="addTask" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useQuasar } from 'quasar'
import axios from 'axios';
import { api } from 'src/boot/axios';
import { useUserStore } from 'src/stores/user';

const $userStore = useUserStore()
const $q = useQuasar()


const tasks = ref([]);



const goodTime = (ISOtime) => {
  return new Date(ISOtime).toLocaleDateString()
}


// update tasks
const update = () => {
  const url = "users/" + $userStore.id
  api.get(url).then(res => {
    const tmp = []
    for (const it of res.data.tasks) {
      const task = {
        id : it.id,
        title: it.title,
        description: it.description,
        deadline: it.deadline,
        is_done: it.is_done,
      }
      tmp.push(task)
    }
    tasks.value = tmp
  }).catch(err => {
    $q.notify('更新失败')
    console.log(err)
  })
}


setInterval(() => {
  update()
}, 1000 * 100)


onMounted(() => {
  update()
})


// finish task
const finishTask = (id) => {
  const url = "tasks/" + id
  api.patch(url, {
  }).then(res => {
    $q.notify('更新成功')

    const task = tasks.value.find(it => it.id === id)
    task.is_done = !task.is_done
  }).catch(err => {
    $q.notify('更新失败')
    console.log(err)
  })
}


// add task
const card = ref(false);
// input
const taskName = ref('');
const taskDeadline = ref('');
const taskDescription = ref('');

const clearInput = () => {
  taskName.value = '';
  taskDeadline.value = '';
  taskDescription.value = '';
}

const addTask = () => {
  if (taskName.value === '') {
    $q.notify('任务名不能为空')
    return;
  }

  if (taskDeadline.value === '') {
    $q.notify('截止时间不能为空')
    return;
  }

  const ISOtime = new Date(taskDeadline.value).toISOString()
  const newtask = {
    id: -1,
    title: taskName.value,
    description: taskDescription.value,
    deadline: ISOtime,
    is_done: false,
  }

  const url = "users/" + $userStore.id + "/tasks"
  api.post(url, {
      title: newtask.title,
      description: newtask.description,
      deadline: newtask.deadline,
  }).then(res => {
    newtask.id = res.data.id
    tasks.value.push(newtask)
    // console.log(res)
    $q.notify('添加成功')
    clearInput()
    update()
  }).catch(err => {
    $q.notify('添加失败')
    console.log(err)
  })
}


const deleteTask = (id) => {
  $q.dialog({
    title: '确认删除',
    message: '你真的要删除这个任务吗?',
    ok: '确定',
    cancel: '取消',
    persistent: true
  }).onOk(() => {
    const url = "tasks/" + id
    api.delete(url, {
    }).then(res => {
      tasks.value = tasks.value.filter(task => task.id !== id)
      $q.notify('任务已删除')
      update()
    }).catch(err => {
      console.log(err)
      $q.notify('删除失败')
    })
  })
}


</script>

<style lang="scss">

.done {
  text-decoration: line-through;
  color: grey;
}

</style>
