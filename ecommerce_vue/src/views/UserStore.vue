<template>
  <div class="users">
  
    <div class="columns is-multiline">
      <div class="column is-12">
          <h2 class=" title is-size-2 has-text-centered">{{username}} Store</h2>
      </div>

      <ProductBox 
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
      Product: [],
      username : this.$route.params.username,     
      myuser: {
        data: 
        {
            username: '',
        }
      }  
    }
  },
  components: {
       ProductBox,
       MyProductBox
  },
  mounted() {
    this.getMyInfo()
    this.getMyProducts()
    document.title = 'My Store | LA'
  },
  methods: {
    async getMyProducts() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get('/api/v1/'+this.username+'/products')
        .then(response => {
          this.Product = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    },
    async getMyInfo() {
    this.$store.commit('setIsLoading', true)
    await axios
        .get('/api/v1/user/info/')
        .then(response => {
            this.myuser = response.data
            if(this.myuser.data.username == this.username){
              this.$router.push('/my-store')
            }
        })
        .catch(error => {
            console.log(error)
        })
        this.$store.commit('setIsLoading', false)
    }
    
  }
}
</script>