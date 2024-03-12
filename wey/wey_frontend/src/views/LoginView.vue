<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div>
            <div class="p-12 bg-white border border-gray-200 rounded-xl">
                <h1 class="mb-6 text-2xl">Log in </h1>

                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem.
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem.
                </p>

                <p class="font-bold">
                   Don't have an account? <RouterLink :to="{'name': 'signup'}" class="underline">Click here</RouterLink> to create one!
                </p>
            </div>
        </div>

        <div>
            <div class="p-12 bg-white border border-gray-200 rounded-xl">
                <form class="space-y-4" v-on:submit.prevent="submitform">
                    <div class="space-y-2">
                        <label class="font-semibold" for="email">E-mail</label><br>
                        <input v-model="form.email" class="w-full mt-2 p-4 border border-gray-200 rounded-lg" placeholder="Your e-mail address" type="email" id="email">
                    </div>

                    <div class="space-y-2">
                        <label class="font-semibold" for="password">Password</label><br>
                        <input v-model="form.password" placeholder="Your password" class="w-full mt-2 p-4 border border-gray-200 rounded-lg" type="password" id="password">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Log in</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
    setup () {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore
        }
    },
    data () {
        return {
            form: {
                email: '',
                password: ''
            },
            errors: []
        }
    },
    methods: {
        async submitform() {
            console.log('from is submitted')
            this.errors = []

            if (this.form.email == ''){
                this.errors.push('email is missing');
            }

            if (this.form.password == ''){
                this.errors.push('password is missing')
            }

            if (this.errors.length === 0){
                await axios
                    .post('api/login/',this.form)
                    .then((response) => {
                        console.log(response.data)
                        this.userStore.setToken(response.data)

                        axios.defaults.headers.common['Authorization'] = "Bearer " + response.data.access;

                    })
                    .catch((error) => {
                        this.errors.push('details not correct')
                        console.log('error',error)

                        this.userStore.removeToken()
                    })

                await axios
                    .get('/api/me/')
                    .then((response) => {
                        console.log(response)
                        this.userStore.setUserInfo(response.data)
                        if (this.userStore.user.isAuthenticated){
                            this.$router.push('/feed');
                        }
                    })
                    .catch((error) => {
                        console.log('error',error)
                    })
                
            }

        }
    }
}
</script>