<template>
    <el-dialog v-model="dialogTableVisible" title="选择文件" width="80vw">
        <el-table :data="tableData" stripe style="width:400 ;" @sort-change="handleSortChange"
            @selection-change="handleSelectionChange" @filter-change="handleFliterChange">
            <el-table-column type="selection" width="44" />
            <el-table-column fixed prop="name" sortable="custom" min-width="90" label="记录名" />
            <el-table-column prop="Comments" label="备注" min-width="70" />
            <el-table-column prop="Type" label="类型" :filters="[
                { text: 'GPX', value: 'GPX' },
                { text: 'FIT', value: 'FIT' },
                { text: 'MP4', value: 'MP4' },
                { text: 'CSV', value: 'CSV' },
                { text: 'Web', value: 'WEB' },
            ]" filter-placement="bottom-start" width="80">
                <template #default="scope">
                    <el-tag
                        :type="scope.row.Type === 'FIT' ? 'primary' : scope.row.Type === 'MP4' ? 'success' : scope.row.Type === 'GPX' ? 'warning' : scope.row.Type === 'CSV' ? 'danger' : 'info'"
                        disable-transitions>{{
                            scope.row.Type
                        }}</el-tag>
                </template>
            </el-table-column>
        </el-table>

        <div style="display:flex; justify-content: space-between; margin-top: 10px;">

            <el-pagination background pager-count="5" layout="prev, pager, next" :total="pages"
                @current-change="changePage" />

            <div>
                <el-select v-model="TimeLineID" placeholder="Select" style="width:100px; margin-right: 10px;">
                    <el-option v-for="item in TimeLineInfo" :key="item.id" :label="item.Name" :value="item.id">
                        <span style="float: left">{{ item.Name }}</span>
                        <span style="
          float: right;
          margin-right: -16px;
          color: var(--el-text-color-secondary);
          font-size: 13px;
        ">{{ item.items }}项</span>
                    </el-option>
                </el-select>
                <el-button type="primary">导入文件</el-button>
                <el-button type="success" @click="proceed">添加选中的文件</el-button>
            </div>
        </div>
    </el-dialog>
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
        const dialogTableVisible = ref(false)
        const TimeLineID = ref('0')
        const TimeLineInfo = ref([
            { id: '0', items: '11', Name: '自动' },
            { id: '1', items: '1', Name: '1' },
            { id: '2', items: '2', Name: '2' },
            { id: '3', items: '3', Name: '3' },
            { id: '4', items: '4', Name: '4' },
        ])
        return {
            tableData,
            selected,
            page,
            order,
            orderBy,
            fliter,
            itemPerPage,
            pages,
            dialogTableVisible,
            TimeLineID,
            TimeLineInfo,
        }
    },
    components: {
    },
    props: {
        cutid: {
            type: String,
            default: ''
        }
    },
    data() {
        return {

        };
    },
    methods: {
        openDialog() {
            this.dialogTableVisible = true;
            this.loadData();
        },
        proceed() {
            let selected = this.selected.map((item) => item.file_id);
            console.log(selected);
            if (selected.length == 0) {
                ElNotification({
                    title: '失败',
                    message: '未选择任何文件',
                    type: 'error'
                });
                return;
            }
            this.$axios.post('/api/addFilesToTimeLine', {
                "TimeLineID": this.TimeLineID,
                "file_ids": selected,
                "cut_id": this.cutid
            }).then((response) => {
                if (response.data.stat == 'OK') {
                    ElNotification({
                        title: '成功',
                        message: '添加成功',
                        type: 'success'
                    });
                    this.dialogTableVisible = false;
                } else {
                    ElNotification({
                        title: '失败',
                        message: response.data.msg,
                        type: 'error'
                    });
                }
            }).catch((error) => {
                ElNotification({
                    title: '失败',
                    message: error,
                    type: 'error'
                });
            });
            this.dialogTableVisible = false;
        },
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
            console.log(this.selected.map((item) => item.file_id));
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
        // this.loadData();
    }
};
</script>

