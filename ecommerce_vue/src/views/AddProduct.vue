<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Add Product</h1>
                <form @submit.prevent="submitForm">
                   
                    <div class="field">
                        <label>Product image</label>
                        <div class="control"> 
                            <input type="file" accept="image/*" @change="uploadImage($event)" id="file-input">
                        </div>
                    </div>
                   
                    <div class="field">
                        <label>Product name</label>
                        <div class="control">
                            <input type="text" class="input" v-model="name">
                        </div>
                    </div>

                      
                    <div class="field">
                        <label>Category</label>
                        <div class="control">
                            <input type="text" class="input" v-model="category">
                        </div>
                    </div>

                    <div class="field">
                        <label>Descripion</label>
                        <div class="control">
                            <input type="text" class="input" v-model="description">
                        </div>
                    </div>
                    
                    <div class="field">
                        <label>Price</label>
                        <div class="control">
                            <input type="number" class="input" :min = "1" :step="0.01" v-model="price">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                    <br><br>
                    <div class="field">
                        <div class="control has-text-centered">
                            <button class="button is-success">Save</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default {
    name: 'AddProduct',
    data() {
        return {
            name: '',
            category: '',
            description: '',
            price: 1,
            image : [],
            errors: [],
            //selectedFile:null,
        }
    },

    mounted() {
        document.title = 'Add Product | LA'
    },

    methods: {
        uploadImage(event) {
            //this.selectedFile=event.target.files[0]
            const URL = 'http://foobar.com/upload'; 

            let data = new FormData();
            data.append('name', 'my-picture');
            data.append('file', event.target.files[0]); 

            let config = {
            header : {
                'Content-Type' : 'image/png'
            }
            }

            axios.put(
            URL, 
            data,
            config
            ).then(
            response => {
                console.log('image upload response > ', response)
            }
            )
        },
        submitForm() {
            this.errors = []
            if (this.name === '') {
                this.errors.push('The name is missing')
            }
            if (this.category=== '') {
                this.errors.push('The category is too short')
            }
            if (this.description=== '') {
                this.errors.push('The description is too short')
            }
            if (this.price < 1) {
                this.errors.push('The price must be positive number')
            }
            if (!this.errors.length) {
                // const fd = new FormData();
                // fd.append('image', this.selectedFile, this.selectedFile.name)
                const formData = {
                    name: this.name,
                    category: this.category,
                    description: this.description,
                    price: this.price,
                    //image: fd
                }
                axios
                    .post(`/api/v1/store/`, formData)
                    .then(response => {
                        toast({
                            message: 'Product added successfully ',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })
                        this.$router.push('/my-store')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
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