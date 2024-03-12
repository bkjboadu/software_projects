<template>
    <div class="grid grid-cols-4 gap-4 ">
        <div class="col-span-3 space-y-4">

            <div class=" p-6 bg-white border border-gray-200 rounded-lg space-y-2">
                <form class="flex space-x-2" v-on:submit.prevent="submitForm">
                    <input type='search' v-model="query" class="rounded-lg bg-gray-200 p-2 border border-gray-100 w-full" placeholder="What are you looking for">

                    <button class="p-6 inline-block text-white bg-purple-600 rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                    </button>
                </form>
            </div>

            <div v-if="this.users_found.length > 0">
                <div class="font-semibold">Users</div>
                <div class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4 space-x-2">                    
                    <div class="bg-gray-200 rounded-lg p-4"  v-for="user in users_found" v-bind:key="user.id">
                        <img src="https://i.pravatar.cc/300?img=70" class="mx-auto rounded-full mb-4">
                        <RouterLink :to="{name: 'profile', params: {'id': user.id}}">
                            <p class="text-center"><strong>{{ user.name }}</strong></p>
                        </RouterLink>
                        

                        <div class="flex space-x-8 justify-around p-4">
                            <p class="text-lg text-gray-500">{{ user.friends_count }} friends</p>
                            <p class="text-lg text-gray-500">120 post</p>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="this.posts_found.length > 0">
                <div class="font-semibold">Posts</div>
                <div class="py-2 px-4 bg-white border border-gray-200 rounded-lg space"  v-for="post in posts_found" v-bind:key="post.id">
                    <Feed v-bind:post="post"/>
                </div>
            </div>
        </div>
        <div class="col-span-1 space-y-4 ">
            <PeopleYouMayKnow />
            <Trend />
        </div>
    </div>
</template>

<script>
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
import Trend from '../components/Trends.vue';
import Feed from '../components/FeedItem.vue'
import axios from 'axios'

export default {
    name: 'SearchView',
    components: {PeopleYouMayKnow,Trend,Feed},
    data() {
        return {
            query: '',
            users_found: [],
            posts_found: []
        }
    },
    methods: {
        submitForm() {
            console.log('query is empty')
            if (this.query != '') {
                axios.post('api/search/',{'query':this.query})
                .then((response) => {
                    this.users_found = response.data.users
                    this.posts_found = response.data.posts

                    console.log(response.data.posts)

                    this.query = ''
                })
                .catch((error) => {
                    console.log('error',error)
                })
            }
        }
    }
}
</script>