<template>
    <div class="column is-3">
     <div class="card" style=" height: 100% ;word-wrap:break-word">
            <div class= "card-content" style="height:70%">
                <figure class="image mb-4">
                    <img :src="product.get_thumbnail">
                </figure>
                <h3 class="is-size-4">{{ product.name }}</h3>
                <p class="is-size-6 has-text-grey">${{ product.price }}</p>
              
            </div>
            <div class="card-footer" style="height:30%">
                <div class="card-footer-item">
                    <router-link v-bind:to="product.get_absolute_url" class="button is-dark mt-4" >View details</router-link>
                </div>
        </div>
     </div>
    </div>
</template>

<script>
export default {
    name: 'ProductBox',
    props: {
        product: Object
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