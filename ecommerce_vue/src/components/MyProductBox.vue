<template>
    <div class="column is-3">
        <div class="box">
            <figure class="image mb-4">
                <img v-bind:src="product.get_thumbnail">
            </figure>

            <h3 class="is-size-4">{{ product.name }}</h3>
            <p class="is-size-6 has-text-grey">${{ product.price }}</p>

            <router-link to="/my-store/add-product" class="button is-dark mt-4">Edit</router-link>
            <router-link to="#" class="button is-danger mt-4">Delete</router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MyProductBox',
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