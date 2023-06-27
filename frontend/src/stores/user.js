import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      isLogin: false,
      id: '',
      email: '',
      username: '',
      admin_type: '',
    }
  },

  persist: true,

  getters: {},

  actions: {
    login (id, email, username, admin_type) {
      this.isLogin = true
      this.id = id
      this.email = email
      this.username = username
      this.admin_type = admin_type
      console.log(this.id, this.email, this.username, this.admin_type)
    },
    logout () {
      this.isLogin = false
      this.email = ''
      this.name = ''
      this.id = ''
    },
  }
})
