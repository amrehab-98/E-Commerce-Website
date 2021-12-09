<template>
  <div class="users">
  
    <div class="columns is-multiline">
      <div class="column is-12">
          <h2 class=" title is-size-2 has-text-centered">My Store</h2>
      </div>

      <div class="column is-12">
          <router-link to="/my-store/add-product/" class="button is-success mt-4 is-pulled-right">Add Product</router-link>
      </div>

       <MyProductBox 
        v-for="product in Product['owned_products']"
        v-bind:key="product.id"
        v-bind:product="product" />

        <ProductBox 
        v-for="product in Product['not_owned_products']"
        v-bind:key="product.id"
        v-bind:product="product" />

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '@/components/ProductBox'
import MyProductBox from '@/components/MyProductBox'
export default {
  name: 'Home',
  data() {
    return {
      Product: {}
    }
  },
  components: {
       ProductBox,
       MyProductBox
  },
  mounted() {
    this.getMyProducts()
    document.title = 'My Store | LA'
  },
  methods: {
    async getMyProducts() {
      this.$store.commit('setIsLoading', true)

      await axios
        .get('/api/v1/store/')
        .then(response => {
          this.Product = response.data
        })
        .catch(error => {
          console.log(error)
        })

      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>