<template>
    <nav class="py-10 borber-b border-gray-200">
        <div class="mx-auto max-w-7xl">
            <div  class="flex items-center justify-between">
                <div>
                    <a href="" class="text-xl font-semibold">Wey</a>
                </div>
                <div class="flex space-x-12" v-if="userstore.user.isAuthenticated">
                    <RouterLink to="/feed">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                        </svg>
                    </RouterLink>
                    <a href="">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.76c0 1.6 1.123 2.994 2.707 3.227 1.068.157 2.148.279 3.238.364.466.037.893.281 1.153.671L12 21l2.652-3.978c.26-.39.687-.634 1.153-.67 1.09-.086 2.17-.208 3.238-.365 1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
                        </svg>
                    </a>
                    <a>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
                        </svg>
                    </a>
                    <RouterLink to="/search">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                    </RouterLink>
                </div>
                <div>
                    <template  v-if="userstore.user.isAuthenticated">
                        <RouterLink :to="{name: 'profile', params: {'id': userstore.user.id}}">
                            <img src="https://i.pravatar.cc/40?img=70" class="rounded-full" >
                        </RouterLink>
                    </template>
                    <template v-else>
                        <RouterLink to="/login" class="mr-4 text-white p-6 bg-gray-600 rounded-lg">Log in </RouterLink>
                        <RouterLink to="/signup" class="p-6 text-white bg-purple-600 rounded-lg">Sign Up </RouterLink>
                    </template>
                    
                </div>
            </div>
        </div>
    </nav>
    <main class="px-8 py-6 bg-gray-100">
        <RouterView />
    </main>

    <Toast />

</template>

<script>
    import Toast from '@/components/Toast.vue'
    import axios from 'axios'
    import { useUserStore } from './stores/user';

    export default {
        setup() {
            const userstore = useUserStore()

            return {
                userstore
            }
        },
        components: {
            Toast
        },
        beforeCreate() {
            // this.userstore.removeToken()
            this.userstore.initStore()

            const token = this.userstore.user.access

            if (token) {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
            } else {
                axios.defaults.headers.common['Authorization'] = "";
            }
        }
    }
</script>
