<template>
    导入数据
    <el-button type="primary" @click="change">
        <el-icon>
            <DocumentCopy />
        </el-icon>从文件中获取</el-button>
    <el-dropdown>
        <el-button type="primary" style="margin-left: 15px;">
            从Internet中获取<el-icon class="el-icon--right"><arrow-down /></el-icon>
        </el-button>
        <template #dropdown>
            <el-dropdown-menu>
                <el-dropdown-item>行者</el-dropdown-item>
                <el-dropdown-item>Strava</el-dropdown-item>
                <el-dropdown-item>Garmin Connect</el-dropdown-item>
                <!-- <el-dropdown-item>Action 4</el-dropdown-item>
                <el-dropdown-item>Action 5</el-dropdown-item> -->
            </el-dropdown-menu>
        </template>
    </el-dropdown>

    <ImportFromFile ref="ImportFromFile"></ImportFromFile>
</template>


<script>

import ImportFromFile from './ImportFromFile.vue'

export default {

    components: {
        ImportFromFile
    },
    // 其他选项...
    data() {
        return {
        };
    },
    methods: {
        change() {
            this.$refs.ImportFromFile.showWindow();
        }

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
</style>
