<template>
    <div class="page-my-account">
        <div class="columns is-multiline">
            <div class="column is-12 has-text-centered" >
                <h1 class="title is-size-2">Admin Panel</h1>
            </div>
            <br> <br> <br><br><br>
            <hr>
            <div class="column is-12 has-text-centered mt-6">
                <h4 class="title"> <strong>Sold History</strong></h4>

                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th width="20%">Product</th>
                            <th width="20%">Price</th>
                            <th width="20%">Seller</th>
                            <th width="20%">Buyer</th>
                            <th width="20%">Purchased Data</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="item in products"
                            v-bind:key="item.id"
                        >
                            <td width="20%">{{ item.name }}</td>
                            <td width="20%">${{ item.price }}</td>
                            <td width="20%">{{ item.get_seller_name }}</td>
                            <td width="20%">{{ item.get_buyer_name }}</td>
                            <td width="20%">{{ format_date(item.date_added) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
export default {
    name: 'Admin',
    data() {
        return {
            products: {},   
        }
    },
    mounted() {
        document.title = 'Admin | LA '
        this.getSoldProducts()
    },
    methods: {
        async getSoldProducts() {
            this.$store.commit('setIsLoading', true)
            await axios
                .get('/api/v1/admin/')
                .then(response => {
                    this.products = response.data
                    console.log(response.data);
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },
        format_date(value) { 
            if (value) { 
                return moment(String(value)).format('MMMM Do YYYY, h:mm:ss a') 
            } 
        }
    }
}
</script>