<template>
    所有工程
    <el-row>
        <el-space wrap :size="small">
            <el-card v-for="item in tableData" :key="item.cut_id" class="box-card" style="width: 250px;">
                <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
                    class="image" />
                <div style="padding: 14px">
                    <div class="ProjName">{{ item.name }}</div>
                    <div class="ProjDesc">{{ item.comments }}</div>
                    <time class="time">{{ item.created_time }}</time>
                    <div class="bottom">

                        <el-button text class="button">打开</el-button>
                        <el-button text class="button">修改</el-button>
                        <el-button text class="button">删除</el-button>
                    </div>
                </div>
            </el-card>
        </el-space>
    </el-row>
</template>


<script>
import { ref } from 'vue'

export default {
    setup() {
        const tableData = ref([])
        // const currentDate = ref(new Date())
        return {
            tableData,
            // currentDate
        }

    },
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
        this.$axios.get('/api/getAllCut').then((response) => {
            console.log(response.data);
            this.tableData = response.data;
        });
    }
};
</script>

<style>
#app {
    max-width: 100%;
    margin: 0 auto;
    padding: 0vw;
}

.time {
    font-size: 10px;
    color: #999;
}

.bottom {
    margin-top: 5px;
    margin-bottom: -20px;
    line-height: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.button {
    padding: 0;
    width: 100px;
    min-height: auto;
}

.image {
    width: 100%;
    height: 100px;
    display: block;
}

.ProjName {
    font-size: 20px;
    font-weight: bold;
}

.ProjDesc {
    font-size: 12px;
    color: #777777;
}
</style>
