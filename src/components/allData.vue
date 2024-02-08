<template>
    所有数据
    <el-button-group class="ml-4">
        <el-button type="primary">
            <el-icon>
                <DocumentAdd />
            </el-icon>
        </el-button>
        <el-button type="primary">
            <el-icon>
                <Delete />
            </el-icon>
        </el-button>
        <el-button type="primary">
            <el-icon>
                <Download />
            </el-icon>
        </el-button>
    </el-button-group>
    <el-table :data="tableData" stripe border style="width: 100%" @sort-change="handleSortChange"
        @selection-change="handleSelectionChange" @filter-change="handleFliterChange">
        <el-table-column type="selection" width="44" />
        <el-table-column fixed prop="name" sortable="custom" label="记录名" width="150" />
        <el-table-column prop="Comments" label="备注" width="120" />
        <el-table-column prop="Type" label="类型" :filters="[
            { text: 'GPX', value: 'GPX' },
            { text: 'FIT', value: 'FIT' },
            { text: 'MP4', value: 'MP4' },
            { text: 'CSV', value: 'CSV' },
            { text: 'Web', value: 'WEB' },
        ]" :filter-method="filterTag" filter-placement="bottom-start" width="80">
            <template #default="scope">
                <el-tag
                    :type="scope.row.Type === 'FIT' ? 'primary' : scope.row.Type === 'MP4' ? 'success' : scope.row.Type === 'GPX' ? 'warning' : scope.row.Type === 'CSV' ? 'danger' : 'info'"
                    disable-transitions>{{
                        scope.row.Type
                    }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="ImportTime" sortable="custom" label="导入时间" width="200" />
        <el-table-column prop="EditTime" sortable="custom" label="修改时间" width="200" />
        <el-table-column prop="Path" label="文件路径" width="300" />
        <el-table-column prop="TimeStart" sortable="custom" label="记录开始时间" width="200" />
        <el-table-column prop="TimeEnd" sortable="custom" label="记录结束时间" width="200" />
        <el-table-column fixed="right" label="Operations" width="170">
            <template #default>
                <el-button link type="primary" size="small">详细信息</el-button>
                <el-button link type="primary" size="small">修改</el-button>
                <el-button link type="primary" size="small">删除</el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-pagination background layout="prev, pager, next" :total="pages" @current-change="changePage" />
    <el-button-group>
        <el-button type="primary"><el-icon>
                <ArrowLeft />
            </el-icon>上一页</el-button>
        <el-button type="primary">
            下一页<el-icon>
                <ArrowRight />
            </el-icon>
        </el-button>
    </el-button-group>
    <el-button type="primary" @click="gotoMainPage">返回主页</el-button>
</template>


<script>

import { ref } from 'vue'
import { ElNotification } from 'element-plus'
import { ElLoading } from 'element-plus'


export default {
    setup() {
        const tableData = ref([])
        const page = ref(1)
        const selected = ref([])
        const order = ref(null)
        const orderBy = ref('')
        const fliter = ref({})
        const itemPerPage = ref(10)
        const pages = ref(100)
        return {
            tableData,
            selected,
            page,
            order,
            orderBy,
            fliter,
            itemPerPage,
            pages
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
        handleFliterChange(filters) {
            this.fliter = [];
            for (let key in filters) {
                this.fliter = filters[key];
            }
            console.log(this.fliter);
            this.loadData();
        },
        handleSortChange({ column, prop, order }) {
            // console.log(column, prop, order);
            column;
            this.order = order;
            this.orderBy = prop;
            this.loadData();
        },
        handleSelectionChange(val) {
            this.selected = val;
            console.log(this.selected);
            console.log(this.selected.map((item) => item.name));
        },
        changePage(i) {
            // console.log(i);
            this.page = i;
            this.loadData();
        },

        // filterTag(value, row) {
        //     return row.Type === value;
        // },
        gotoMainPage() {
            this.$emit('gotoPage', 0);
        },
        loadData() {
            const loading = ElLoading.service({
                lock: true,
                text: '正在获取文件列表,请稍后...',
                background: 'rgba(0, 0, 0, 0.7)',
            })
            try {
                this.$axios.post('/api/getFileList', {
                    "fliter": this.fliter,
                    "order": this.order,
                    "orderBy": this.orderBy,
                    "page": this.page,
                    "itemPerPage": this.itemPerPage
                }).then((response) => {
                    if (response.data.stat == 'OK') {
                        this.tableData = response.data.data.items;
                        this.pages = response.data.data.pages;
                        console.log(response.data.data);
                        loading.close()
                    } else {
                        ElNotification({
                            title: 'ERROR!',
                            message: response.data.msg,
                            type: 'error',
                        })
                        loading.close()
                    }
                });
            } catch (error) {
                ElNotification({
                    title: '出错了!',
                    message: error,
                    type: 'error',
                })
                loading.close()
            }
        }

    },
    mounted() {
        this.loadData();
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
