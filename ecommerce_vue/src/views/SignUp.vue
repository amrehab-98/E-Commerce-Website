<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Sign up</h1>

                <form @submit.prevent="submitForm">
                   
                    <div class="field">
                        <label>First name</label>
                        <div class="control">
                            <input type="text" class="input" v-model="first_name">
                        </div>
                    </div>

                    <div class="field">
                        <label>Last name</label>
                        <div class="control">
                            <input type="text" class="input" v-model="last_name">
                        </div>
                    </div>

                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>
                    
                    <div class="field">
                        <label>Email</label>
                        <div class="control">
                            <input type="email" class="input" v-model="email">
                        </div>
                    </div>
                    
                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="field">
                        <label>Confirm password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="confirm_password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Sign up</button>
                        </div>
                    </div>

                    <hr>

                    Or <router-link to="/log-in">click here</router-link> to log in!
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default {
    name: 'SignUp',
    data() {
        return {
            email : '',
            first_name: '',
            last_name: '',
            username: '',
            password: '',
            confirm_password: '',
            errors: []
        }
    },

    mounted() {
        document.title = 'Sign Up | LA'
    },

    methods: {
        submitForm() {
            this.errors = []
            if (this.username === '') {
                this.errors.push('The username is missing')
            }
            if (this.first_name === '') {
                this.errors.push('The firstname is missing')
            }
            if (this.last_name === '') {
                this.errors.push('The lastname is missing')
            }
            if (this.email === '') {
                this.errors.push('The email is missing')
            }
            if (this.password === '') {
                this.errors.push('The password is too short')
            }
            if (this.password !== this.confirm_password) {
                this.errors.push('The passwords doesn\'t match')
            }
            if (!this.errors.length) {
                const formData = {
                    username: this.username,
                    first_name: this.first_name,
                    last_name: this.last_name,
                    email: this.email,
                    password: this.password,
                    confirm_password: this.confirm_password
                }
                axios
                    .post("/api/v1/register/", formData)
                    .then(response => {
                        toast({
                            message: 'Account created, please log in!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })
                        const token = response.data.token
                        this.$store.commit('setToken', token)
                    
                        axios.defaults.headers.common["Authorization"] = "Token " + token
                        localStorage.setItem("token", token)
                        this.$router.push('/')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data.data) {
                                this.errors.push(`${property}: ${error.response.data.data[property]}`)
                            }   
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')
                            
                            console.log(JSON.stringify(error))
                        }
                    })
            }
        }
    }
}
</script>