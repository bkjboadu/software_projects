<template>
    <div class="flex items-center justify-between mb-4">
        <div class="flex space-x-4 items-center ">
            <img src="https://i.pravatar.cc/40?img=70" class="rounded-full">
            <RouterLink :to="{name: 'profile', params: {'id': post.created_by.id}}">
                <p class="font-semibold">{{ post.created_by.name }}</p>
            </RouterLink>
        </div>
        <div>
            <p class="text-gray-400">{{ post.created_at_formatted }}</p>
        </div>
    </div>
    <div class="mb-4">
        <p>{{ post.body }}</p>
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
                    <p class="inline-block">82 likes</p>
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
                <a href="">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                    </svg>
                </a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        post: Object
    }
}
</script>