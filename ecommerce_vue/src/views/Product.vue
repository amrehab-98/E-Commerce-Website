<template>
    <div class="page-product">
        <div class="columns is-multiline">
            <div class="column is-9">
                <figure class="image mb-6">
                    <img v-bind:src="product.get_image">
                </figure>

                <h1 class="title">{{ product.name }}</h1>

                <p>{{ product.description }}</p>
            </div>

            <div class="column is-3">
                <h2 class="subtitle">Information</h2>

                <p><strong>Price: </strong>${{ product.price }}</p>

                <div class="field has-addons mt-6">
                    <div class="control">
                        <a class="button is-dark" @click="addToCart()">Add to cart</a>
                    </div>
                </div>
                <div class="field has-addons mt-3">
                    <div class="control" v-if="!isHidden">
                        <a class="button is-dark" @click="addToMyStore()">Add to my store</a>
                    </div>
                    <div class="control" v-else>
                        <a class="button is-danger" @click="RemoveFromMyStore()">Remove from my store</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template> 

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default {
    name: 'Product',
    data() {
        return {
            product: {},
            quantity: 1,
            user: {},
            isHidden: false
        }
    },
    // created() {
    //     this.getProduct().then(response=>{
    //         console.log(this.user.not_owned_products)
    //         for (var i = 0; i < this.user.not_owned_products.length; i++) {
    //             if (this.product.id == this.user.not_owned_products[i].id) {
    //                 this.isHidden = true
    //             }  
    //         }
    //     })
        
    // },
    mounted() {  
        this.getProduct().then(response=>{
        for (var i = 0; i < this.user.not_owned_products.length; i++) {
            if (this.product.id == this.user.not_owned_products[i].id) {
                this.isHidden = true
            }  
        }
    })    
    },
    methods: {
        async getProduct() {
            this.$store.commit('setIsLoading', true)
            const username = this.$route.params.username
            const id = this.$route.params.id
            await axios
                .get(`/api/v1/${username}/products/${id}`)
                .then(response => {
                    this.product = response.data.product
                    this.user = response.data.user
                    document.title = this.product.name + ' | LA'
                })
                .catch(error => {
                    console.log(error)
                })
            
            this.$store.commit('setIsLoading', false)
        },
        addToCart() {
            if (isNaN(this.quantity) || this.quantity < 1) {
                this.quantity = 1
            }
            const item = {
                product: this.product,
                quantity: this.quantity
            }
            this.$store.commit('addToCart', item)
            toast({
                message: 'The product was added to the cart',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-right',
            })
        },
        async addToMyStore() {
            this.$store.commit('setIsLoading', true)
            const id = this.$route.params.id
            console.log(id*2);
            const info = {
                id: id
            }
            await axios
                .post(`/api/v1/products/addtomystore/`, info)
                .then(response => {
                    console.log("I am here");
                    this.$router.push('/my-store')
                })
                .catch(error => {
                    console.log(error)
                })
            
            this.$store.commit('setIsLoading', false) 
        },
        async RemoveFromMyStore() {
            this.$store.commit('setIsLoading', true)
            const id = this.$route.params.id
            console.log(id*2);
            const info = {
                id: id
            }
            await axios
                .post(`/api/v1/products/removefrommystore/`, info)
                .then(response => {
                    console.log("I am here");
                    this.$router.push('/my-store')
                })
                .catch(error => {
                    console.log(error)
                })
            
            this.$store.commit('setIsLoading', false) 
        },
    }
}
</script>