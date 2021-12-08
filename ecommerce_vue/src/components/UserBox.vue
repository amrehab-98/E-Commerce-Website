<template>
    <div class="column is-3">
        <div class="box">
            <figure class="image mb-4">
                <img v-bind:src="product.get_thumbnail">
            </figure>

            <h3 class="is-size-4">{{ myuser.first_name }}</h3>

            <router-link v-bind:to="myuser.get_absolute_url" class="button is-dark mt-4">View Store</router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'UserBox',
    props: {
        myuser: Object
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