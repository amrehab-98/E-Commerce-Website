<template>
  <div class="users">
  
    <div class="columns is-multiline">
      <div class="column is-12">
          <h2 class="title is-size-2 has-text-centered">{{myuser.first_name}} Store</h2>
      </div>

       <ProductBox 
        v-for="product in Products"
        v-bind:key="product.id"
        v-bind:product="product" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '@/components/ProductBox'
export default {
  name: 'UserStore',
  data() {
    return {
      Products: [],
      myuser: {}
    }
  },
  components: {
       ProductBox
  },
  mounted() {
    this.getProducts()
    document.title = this.myuser.username + ' | LA'
  },
  methods: {
    async getProducts() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get('/api/v1/')
        .then(response => {
          this.Products = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>