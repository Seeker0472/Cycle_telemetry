<template>
    <div class="con">
        <div class="Buttons">
            <el-button color="#626aef" plain @click="gotoPage(1)"> <el-icon>
                    <Plus />
                </el-icon>导入数据</el-button>
            <el-button color="#626aef" plain @click="gotoPage(2)">创建工程</el-button>
            <el-button color="#626aef" plain @click="gotoPage(3)">所有数据</el-button>
            <el-button color="#626aef" plain @click="gotoPage(4)">所有工程</el-button>
            <el-button color="#626aef" plain @click="gotoPage(5)">同步</el-button>
            <el-button color="#626aef" plain @click="gotoPage(6)">关于</el-button>
        </div>
    </div>
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
        gotoPage(i) {
            this.$emit('gotoPage', i);
        }

    },
    mounted() {

    }
};
</script>

<style>
.con {
    width: calc(100% - 16px);
    height: calc(100% - 16px);
    /* background-color: #00ff00; */
    display: block;
    position: absolute;
    margin: 0px;
}

.buttons {

    display: flex;
    justify-content: center;
    align-items: center;
}

#app {
    max-width: 100%;
    margin: 0 auto;
    padding: 0vw;
}
</style>
