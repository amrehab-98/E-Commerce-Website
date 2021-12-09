<template>
    <div class="column is-3">
        <div class="box">
            <figure class="image mb-4">
                <img v-bind:src="product.get_thumbnail">
            </figure>

            <h3 class="is-size-4">{{ product.name }}</h3>
            <p class="is-size-6 has-text-grey">${{ product.price }}</p>
            
            <router-link to="#" class="button is-dark mt-4">Edit</router-link>
            <router-link to="#" class="button is-danger mt-4" @click = "deleteProduct(product.id)">Delete</router-link>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'MyProductBox',
    props: {
        product: Object
    },
    methods:{
        async deleteProduct(id) {
        this.$store.commit('setIsLoading', true)
        await axios
        .delete(`/api/v1/product/${id}`)
        .then(response => {
        console.log(response)
        })
        .catch(error => {
        console.log(error)
        })
        this.$store.commit('setIsLoading', false)
        this.$router.go()
        },
       
    }
  
}

</script>

<style scoped>
  .image {
    margin-top: -1.25rem;
    margin-left: -1.25rem;
    margin-right: -1.25rem;
  }
</style>