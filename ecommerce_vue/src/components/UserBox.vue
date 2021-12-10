<template>
    <div class="column is-3">
        <div class="card" style="height:100% ;word-wrap:break-word">
            <div class ="card-content" >
            <h3 class="is-size-4">{{ myuser.username }}</h3>
            <p class="is-size-6 has-text-grey">{{ myuser.get_name }}</p>
            <p class="is-size-6 has-text-grey">{{ myuser.email}}</p>
            </div>
            <div class="card-footer">
                <div class = "card-footer-item" >
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