<template>
    <div class="page-my-account">
        <div class="columns is-multiline">
            <div class="column is-12 has-text-centered" >
                <h1 class="title is-size-2">My Account</h1>
            </div>
           <br> <br> <br><br><br>
           <div class = "column is-12 box">
                <div class="column is-12">
                    <h2 class = "subtitle" ><strong>Name: </strong> {{myuser.first_name+' '+myuser.last_name}}</h2>
                </div>

                <div class="column is-12">
                    <h2 class = "subtitle" ><strong>Email:</strong>{{myuser.email}}</h2>
                </div>
                <div class="column is-12">
                    <h2 class = "subtitle" ><strong>Balance:</strong> {{myuser.balance}}</h2>
                </div>
                <div class="column is-12">
                    <button class="button is-dark" @click="BuyCoins">Buy Coins</button>
                </div>
           </div>

            <hr>
            <br><br><br><br>
            <div class="column is-12 has-text-centered">
                <h4 class="title"> <strong> Orders</strong></h4>

                <OrderSummary
                    v-for="order in orders"
                    v-bind:key="order.id"
                    v-bind:order="order" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import OrderSummary from '@/components/OrderSummary.vue'
export default {
    name: 'MyAccount',
    components: {
        OrderSummary
    },
    data() {
        return {
            orders: [],
            myuser : {}
        }
    },
    mounted() {
        document.title = 'My Account | LA '
        this.getMyOrders()
    },
    methods: {
        async getMyOrders() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get('/api/v1/orders/')
                .then(response => {
                    this.orders = response.data
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>