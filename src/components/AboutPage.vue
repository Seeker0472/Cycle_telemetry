<!-- <template>
    关于页面
</template>


<script>
export default {
    components: {
    },
    // 其他选项...
    data() {
        return {

        };
    },
    methods: {

    },
    mounted() {

    }
};
</script>

<style>
#app {
    max-width: 100%;
    margin: 0 auto;
    padding: 0vw;
}
</style> -->

<template>
    <form @submit.prevent="onSubmit">
        <input v-model="value" />

        <button type="submit" :disabled="isLoading">Submit</button>
    </form>
</template>

<script>
import { socket } from "@/socket";

export default {
    name: "MyForm",

    data() {
        return {
            isLoading: false,
            value: ""
        }
    },

    methods: {
        onSubmit() {
            // this.isLoading = true;

            socket.timeout(5000).emit("message", this.value, (err, response) => {
                this.isLoading = false;

                console.log(response);
            });
        },
    }
}
</script>