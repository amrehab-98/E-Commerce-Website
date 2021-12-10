<template>
    <div class="column is-3">
           
        <div class="card" style="height:100%; width:100% ;word-wrap:break-word">
            <div class="card-content" style="height:70%">
                <figure class="image mb-4">
                    <img v-bind:src="product.get_thumbnail">
                </figure>

                <h3 class="is-size-4">{{ product.name }}</h3>
                <p class="is-size-6 has-text-grey">${{ product.price }}</p>
            </div>
            <div class="card-footer">
                <div class ="card-footer-item" style="height:30%"> 
                    <router-link v-bind:to="'/my-store/edit-product/'+product.id" class="button is-dark mt-3" style="width:25% ;margin-right:10px">Edit</router-link>
                    <router-link to="#" class="button is-danger mt-3" @click = "deleteProduct(product.id)" style=" margin-left:10px">Delete</router-link>
                </div>
            </div>
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