import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      isLogin: false,
      id: '',
      email: '',
      name: '',
    }
  },

  persist: true,

  getters: {},

  actions: {
    login (id, email, name) {
      this.isLogin = true
      this.id = id
      this.email = email
      this.name = name
    },
    logout () {
      this.isLogin = false
      this.email = ''
      this.name = ''
      this.id = ''
    },
  }
})
