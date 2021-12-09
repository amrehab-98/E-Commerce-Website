<template>
  <div class="users">
  
    <div class="columns is-multiline">
      <div class="column is-12">
          <h2 class=" title is-size-2 has-text-centered">Users</h2>
      </div>

      <UserBox :username="myuser.username"
        v-for="myuser in Users"
        v-bind:key="myuser.id"
        v-bind:myuser="myuser" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import UserBox from '@/components/UserBox'
export default {
  name: 'Home',
  data() {
    return {
      Users: []
    }
  },
  components: {
       UserBox
  },
  mounted() {
    this.getUsers()
    document.title = 'Users | LA'
  },
  methods: {
    async getUsers() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get('/api/v1/stores/')
        .then(response => {
          this.Users = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>