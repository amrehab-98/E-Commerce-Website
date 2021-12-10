<template>
    <div class="column is-3">
        <div class="card" style="height:100% ;word-wrap:break-word">
            <div class ="card-content" style="height:60%">
            <h3 class="is-size-4">{{ myuser.username }}</h3>
            </div>
            <div class="card-footer">
                <div class = "card-footer-item" style="height:40%">
                    <router-link v-bind:to="'/users/'+myuser.username" class="button is-dark mt-4">View Store</router-link>
                </div>
            </div>   
        
        </div>
    </div>
</template>

<script>
export default {
    name: 'UserBox',
    props: {
        myuser: Object
    },

}
</script>

<style scoped>
  .image {
    margin-top: -1.25rem;
    margin-left: -1.25rem;
    margin-right: -1.25rem;
  }
</style>