<template>
    <v-banner 
        color="primary" 
        class="elevation-5 px-10 mb-6"
    >
        <span class="white--text text-h4 px-10">
            {{title}}
        </span>
    </v-banner>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true
        },
    },
}
</script>

<style scoped></style>
