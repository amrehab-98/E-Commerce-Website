<template>
  <div class="home">
    <section class="hero is-small is-dark mb-6">
        <div class="hero-body has-text-centered">
            <p class="title mb-6">
                Welcome to LA Store
            </p>
            <p class="subtitle">
                The best online store
            </p>
        </div>
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
          <h2 class="is-size-2 has-text-centered"> Products</h2>
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
  name: 'Home',
  data() {
    return {
      Products: []
    }
  },
  components: {
    ProductBox
  },
  mounted() {
    this.getProducts()
    document.title = 'Home | LA'
  },
  methods: {
    async getProducts() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get('/api/v1/products/')
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

