<template>
    <div class="page-my-account">
        <div class="columns is-multiline">
            <div class="column is-12 has-text-centered" >
                <h1 class="title is-size-2">My Account</h1>
            </div>
           <br> <br> <br><br><br>
           <div class = "column is-12 box">
                <div class="column is-12">
                    <h2 class = "subtitle" ><strong>Name: </strong>{{myuser.data.get_name}}</h2>
                </div>
                <div class="column is-12">
                    <h2 class = "subtitle" ><strong>Username: </strong>{{myuser.data.username}}</h2>
                </div>

                <div class="column is-12">
                    <h2 class = "subtitle" ><strong>Email: </strong>{{myuser.data.email}}</h2>
                </div>
                <div class="column is-12">
                    <h2 class = "subtitle" ><strong>Balance: </strong>${{myuser.data.get_balance}}</h2>
                </div>
                 
                <div class="column is-12">
                    <router-link to="/my-account/charge-balance" class="button is-dark" @click="BuyCoins">Charge Balance</router-link>
                </div>
                <hr>

           </div>

            <hr>
            <br><br><br><br>
            <div class="column is-12 has-text-centered">
                <h4 class="title"> <strong>Purchase History</strong></h4>

                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th width="33%">Product</th>
                            <th width="33%">Price</th>
                            <th width="33%">Seller</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="item in products.purchased"
                            v-bind:key="item.id"
                        >
                            <td width="33%">{{ item.name }}</td>
                            <td width="33%">${{ item.price }}</td>
                            <td width="33%">{{ item.get_seller_name }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <hr>
            <div class="column is-12 has-text-centered mt-6">
                <h4 class="title"> <strong>Sold History</strong></h4>

                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th width="33%">Product</th>
                            <th width="33%">Price</th>
                            <th width="33%">Buyer</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="item in products.sold"
                            v-bind:key="item.id"
                        >
                            <td width="33%">{{ item.name }}</td>
                            <td width="33%">${{ item.price }}</td>
                            <td width="33%">{{ item.get_buyer_name }}</td>
                        </tr>
                    </tbody>
                </table>
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
            products: {},
            myuser : {
                data : {
                    get_name: '',
                    username: '',
                    get_balance: 0,
                    email : '',
                }
            }
        }
    },
    mounted() {
        document.title = 'My Account | LA '
        this.getMyOrders()
        this.getMyInfo()
    },
    methods: {
        async getMyOrders() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get('/api/v1/orders/')
                .then(response => {
                    this.products = response.data
                    console.log(response.data);
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
                console.log("request sent")
                console.log(this.myuser.data.get_name)
            })
            .catch(error => {
                console.log(error)
            })
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>