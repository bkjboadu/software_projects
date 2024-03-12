<template>
    <div class="grid grid-cols-4 gap-4">
        <div class="col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <form method="post" v-on:submit.prevent='submitForm'>
                    <div class="p-4">
                        <textarea  placeholder="What are you thinking about?" v-model="body" class="w-full bg-gray-100 rounded-lg p-6"></textarea>
                    </div>
                    <div class="p-4 flex justify-between border-t border-gray-100">
                        <a href="" class="px-6 py-4 inline-block rounded-lg bg-gray-600 text-white">Attach image</a>
                        <button href="" class="px-6 py-4 inline-block rounded-lg bg-purple-600 text-white">Post</button>
                    </div>
                </form>
            </div>
            <div v-if="posts.length > 0" class="space-y-4">
                <div class="py-2 px-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                    <Feed v-bind:post="post" />
                </div>
            </div>
            <div class="py-2 px-4 bg-white border border-gray-200 rounded-lg">
                <div class="flex items-center justify-between mb-4">
                    <div class="flex space-x-4 items-center ">
                        <img src="https://i.pravatar.cc/40?img=70" class="rounded-full">
                        <p class="font-semibold">Code With Bright</p>
                    </div>
                    <div>
                        <p class="text-gray-400">18 minutes ago</p>
                    </div>
                </div>
                <div class="mb-4">
                    <img src="https://i.pravatar.cc/500?img=70" class="mx-auto rounded-full mb-4">
                </div>
                <div>
                    <div class="flex justify-between items-center">
                        <div class="flex items-center justify-around space-x-6">
                            <div class="flex space-x-2">
                                <a href="">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                                    </svg>
                                </a>  
                                <p class="inline-block">{{ post.likes_count }}</p>
                            </div>
                            <div class="flex space-x-2">
                                <a href=" ">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 0 1-.923 1.785A5.969 5.969 0 0 0 6 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337Z" />
                                    </svg>
                                </a>
                                <p>0 comments</p>
                            </div>
                        </div>
                        <div>
                            <a>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                                </svg>

                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
        <div class="col-span-1 space-y-4 ">
            <PeopleYouMayKnow />
            <Trends/>
        </div>
    </div>
</template>

<script>
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue"
import Trends from '../components/Trends.vue'
import Feed from '../components/FeedItem.vue'

import { useToastStore } from "@/stores/toast";
import { useUserStore } from '@/stores/user';
import axios from 'axios';


export default {
    name: 'FeadView',
    components: {PeopleYouMayKnow,Trends,Feed},
    setup() {
        const toastStore = useToastStore()
        const userstore = useUserStore()

        return {
            toastStore,
            userstore
        }
    },
    data() {
        return {
            body: '',
            posts: []
        }
    },
    mounted() {
        this.getFeed();
        if (this.userstore.user.isAuthenticated){
            this.toastStore.showToast(5000,`${this.userstore.user.name} is logged in`,'bg-emerald-500');
        }
    },
    methods: {
        getFeed(){
            axios
            .get('api/posts/')
            .then((response) => {
                console.log('data',response)
                this.posts = response.data
            })
            .catch((error) => {
                console.log('error',error)
            })
        },
        submitForm() {
            
            axios
            .post('api/posts/create/',{body: this.body})
            .then((response) => {
                this.body = ''
                this.posts.unshift(response.data)
            })
            .catch((error) => {
                console.log('error',error)
            })
        }

    }
}
</script>