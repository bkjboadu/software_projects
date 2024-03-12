<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div>
            <div class="p-12 bg-white border border-gray-200 rounded-xl">
                <h1 class="mb-6 text-2xl">Sign Up</h1>

                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem.
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem.
                </p>

                <p class="font-bold">
                   Already have an account? <RouterLink :to="{'name': 'login'}" class="underline">Click here </RouterLink> to log in!
                </p>
            </div>
        </div>

        <div>
            <div class="p-12 bg-white border border-gray-200 rounded-xl">
                <form class="space-y-4" v-on:submit.prevent="submitForm">
                    <div class="space-y-2">
                        <label class="font-semibold" for="name">Name</label><br>
                        <input class="w-full mt-2 p-4 border border-gray-200 rounded-lg" placeholder="Your Full name" type="text" id="name" v-model="form.name">
                    </div>

                    <div class="space-y-2">
                        <label class="font-semibold" for="email">E-mail</label><br>
                        <input class="w-full mt-2 p-4 border border-gray-200 rounded-lg" placeholder="Your e-mail address" type="email" id="email" v-model="form.email">
                    </div>
                    
                    <div class="space-y-2">
                        <label class="font-semibold" for="repeat_password">Password</label><br>
                        <input placeholder="password" v-model="form.password1" class="w-full mt-2 p-4 border border-gray-200 rounded-lg" type="password" id="repeat_password">
                    </div>

                    <div class="space-y-2">
                        <label class="font-semibold" for="password">Repeat Password</label><br>
                        <input placeholder="repeat password" v-model="form.password2" class="w-full mt-2 p-4 border border-gray-200 rounded-lg" type="password" id="password">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign Up</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { useToastStore } from '@/stores/toast';
import axios from 'axios'

export default {
    setup() {
        const toastStore = useToastStore()

        return {toastStore}
    },

    data () {
        return {
            form: {
                email: '',
                name: '',
                password1: '',
                password2: ''
            },
            errors: []
        }
    },
    methods: {
        submitForm () {
            this.errors = []
            if (this.form.email == '') {
                this.errors.push('your email is missing')
            }

            if (this.form.name == '') {
                this.errors.push('your name is missing')
            }

            if (this.form.password1 == '') {
                this.errors.push('Your password is missing')
            }

            if (this.form.password1 != this.form.password2) {
                this.errors.push('The password does not match')
            }

            if (this.errors.length == 0) {
                axios.post('api/signup/', this.form)
                .then((response) => {
                    console.log('Response:', response.data);
                    if (response.data.status === 'success') {
                        console.log("It's done")
                        this.toastStore.showToast(5000,'The user is registered. Please log in','bg-emerald-500')
                        this.form.email = ''
                        this.form.name = ''
                        this.form.password1 = ''
                        this.form.password2 = ''

                        this.$router.push('/login')
                    } else {
                        this.toastStore.showToast(5000,'Something went wrong. Please try again','bg-red-300')
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