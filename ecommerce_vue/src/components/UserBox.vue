<template>
    <div class="column is-3">
        <div class="box">

            <h3 class="is-size-4">{{ myuser.username }}</h3>

            <router-link v-bind:to="'/users/'+myuser.username" class="button is-dark mt-4">View Store</router-link>
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