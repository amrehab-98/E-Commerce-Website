<template>
    <div class="page-my-account">
        <div class="columns is-multiline">
            <div class="column is-12 has-text-centered" >
                <h1 class="title is-size-2">Charge Balance</h1>
            </div>
           <br> <br> <br><br><br>

           <div class="notification is-danger mt-4 column is-12" v-if="errors.length">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
           
           <div class = "column is-12 box">
                <div class="column is-12">
                    <label class="label">Enter Amount</label>
                    <input class = "input" type="number" :min="50" v-model="amount">
                </div>

                 <hr>

                <div id="card-element" class="mb-5"></div>
            
                
                <div class="column is-12">
                    <button class="button is-dark" @click="checkout">Pay with stripe</button>
                </div>
           </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
export default {
    name: 'ChargeBalance',
    data() {
        return {
            stripe: {},
            amount:50, 
            errors: []
        }
    },
    mounted() {
        document.title = 'Charge Balance | LA '
        this.stripe = Stripe('pk_test_51K4nGfIsQIccppgRykGTcGtPSuyfzK5othBkQCgqGGkXYhrFQxSO3oKeqKpN74Zav22yOnUOcgtCZDc3mhiKAJci0092N5WzGD')
        const elements = this.stripe.elements();
        this.card = elements.create('card', { hidePostalCode: true })
        this.card.mount('#card-element')
    },
    methods: {
        checkout() {
            this.$store.commit('setIsLoading', true)
            this.stripe.createToken(this.card).then(result => {                    
                if (result.error) {
                    this.$store.commit('setIsLoading', false)
                    this.errors.push('Something went wrong with Stripe. Please try again')
                    console.log(result.error.message)
                } else {
                    this.stripeTokenHandler(result.token)
                }
            })
        },
         async stripeTokenHandler(token) {
            const data = {
                'amount': this.amount,
                'stripe_token': token.id,
            }
            await axios
                .post('/api/v1/account/charge/', data)
                .then(response => {
                    toast({
                        message: 'Balance charged successufelly',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 4000,
                        position: 'top-center',
                        fullWidth: true,
                        fitToScreen: true,
                    })
                    this.$router.push('/my-account')
                })
                .catch(error => {
                    this.errors.push('Something went wrong. Please try again')
                    console.log(error)
                })
                this.$store.commit('setIsLoading', false)
        }
    },
}
</script>