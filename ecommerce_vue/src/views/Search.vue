<template>
    <div class="page-search">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Search</h1>

                <h2 class="is-size-5 has-text-grey">Search term: "{{ query }}"</h2>
            </div>
            <div class="columns is-multiline">
            <ProductBox 
                v-for="product in products.products"
                v-bind:key="product.id"
                v-bind:product="product" />
            </div>
            <div class="columns is-multiline">
            <UserBox :username="products.users.username"
                    v-for="myuser in products.users"
                    v-bind:key="myuser.id"
                    v-bind:myuser="myuser" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import ProductBox from '@/components/ProductBox.vue'
import UserBox from '@/components/UserBox.vue'
export default {
    name: 'Search',
    components: {
        ProductBox,
        UserBox,
    },
    data() {
        return {
            products: [],
            query: ''
        }
    },
    mounted() {
        document.title = 'Search | Products'
        let uri = window.location.search.substring(1)
        let params = new URLSearchParams(uri)
        if (params.get('query')) {
            this.query = params.get('query')
            this.performSearch()
        }
    },
    methods: {
        async performSearch() {
            this.$store.commit('setIsLoading', true)
            await axios
                .post('/api/v1/search/', {'query': this.query})
                .then(response => {
                    this.products = response.data
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        }
    }
}
</script>