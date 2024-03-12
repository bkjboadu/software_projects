<template>
    <div class="grid grid-cols-4 gap-4">
        <div class="col-span-1">
            <div class=" p-6 bg-white border border-gray-200 rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mx-auto rounded-full mb-4">

                <p class="text-center"><strong>{{ profile_user.name }}</strong></p>

                <div class="flex space-x-8 justify-around p-4">
                    <p class="text-xs text-gray-500">{{ profile_user.friends_count }} friends</p>
                    <p class="text-xs text-gray-500">120 post</p>
                </div>

            </div>
        </div>
        <div class="col-span-2 space-y-4">
            <div v-if="this.friend_requests.length > 0">
                <div class="font-semibold">Friend Requests</div>
                <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="friend_request in this.friend_requests" v-bind:key="friend_request.id" :current_friend="friend_request">
                    <div class="flex justify-between items-center">
                        <div class="flex justify-between items-center space-x-4">
                            <img src="https://i.pravatar.cc/40?img=70" class="rounded-full">
                            <RouterLink :to="{name: 'profile', params: {'id': friend_request.created_by.id}}">
                                <p class="text-center"><strong>{{ friend_request.created_by.name }}</strong></p>
                            </RouterLink>
                        </div>
                        <div class="space-x-2">
                            <button class="p-4 bg-purple-600 text-white rounded-xl" @click="handleRequest('accepted',friend_request)">Accept</button>
                            <button class="p-4 bg-red-600 text-white rounded-xl" @click="handleRequest('rejected',friend_request)">Reject</button>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="this.friends.length > 0">
                <div class="font-semibold">Friends</div>
                <div class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4 space-x-2" >
                    <div class="bg-gray-200 rounded-lg p-4"  v-for="friend in this.friends" v-bind:key="friend.id">
                        <img src="https://i.pravatar.cc/300?img=70" class="mx-auto rounded-full mb-4">

                        <RouterLink :to="{name: 'profile', params: {'id': friend.id}}">
                            <p class="text-center"><strong>{{ friend.name }}</strong></p>
                        </RouterLink>

                        <div class="flex space-x-8 justify-around p-4">
                            <p class="text-xs text-gray-500">{{ friend.friends_count }} friends</p>
                            <p class="text-xs text-gray-500">120 post</p>
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
    name: 'FriendsView',
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
            profile_user: {},
            friend_requests: [],
            friends: [],
            current_friend: {}
        }
    },
    mounted() {
       this.getFriends()
    },
    methods: {
        getFriends(){
            axios
                .get(`api/friends/${this.$route.params.id}/`)
                .then((response) => {
                    console.log(response.data)

                    this.profile_user = response.data.user
                    this.friends = response.data.friends
                    console.log(response.friends)
                    

                    if (response.data.friend_request){
                        this.friend_requests = response.data.friend_request
                        console.log(response.data.friend_request)
                        
                    }

                })
                .catch((error)=> {
                    console.log('error',error)
                })
        },
        handleRequest(status,pk){
            axios
                .post(`api/friends/${pk.created_by.id}/${status}/`)
                .then((response)=> {
                    console.log(response.data)

                    this.friend_requests.shift()

                    const current_friend = pk

                    if (status == 'accepted') {
                        this.profile_user.friends_count += 1
                        console.log(current_friend)
                        this.friends.push(current_friend)
                        // console.log(this.current_friend)
                    }
                })
                .catch((error) => {
                    console.log('error',error)
                })
        }
    }
}
</script>