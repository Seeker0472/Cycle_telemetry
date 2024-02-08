<template>
    <el-dialog v-model="centerDialogVisible" title="请确认详细信息" width="500" align-center>
        <span>名字</span>
        <el-input v-model="name" placeholder="取一个名字吧~" />
        <span>描述</span>
        <el-input v-model="description" placeholder="描述一下这个项目吧~" />
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="centerDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="proceed">
                    确定
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>


<script>
import { ref } from 'vue'
import { ElNotification } from 'element-plus'
import { ElLoading } from 'element-plus'

export default {
    setup() {
        const centerDialogVisible = ref(false)
        const name = ref('')
        const description = ref('')

        return {
            centerDialogVisible,
            name,
            description
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
        showWindow() {
            this.centerDialogVisible = true;
        },
        proceed() {
            if (this.name === '') {
                ElNotification({
                    title: '名字不能为空!',
                    message: '给项目取一个名字吧~',
                    type: 'error'
                });
                return;
            }
            const loading = ElLoading.service({
                lock: true,
                text: '请稍后...',
                background: 'rgba(0, 0, 0, 0.7)',
            })
            this.$axios.post('/api/addCut', {
                name: this.name,
                description: this.description
            }).then(res => {
                if (res.data.stat === 'OK') {
                    ElNotification({
                        title: '成功!',
                        message: '项目创建成功',
                        type: 'success'
                    });
                    this.centerDialogVisible = false;
                    loading.close();
                } else {
                    ElNotification({
                        title: '创建项目失败!',
                        message: res.data.msg,
                        type: 'error'
                    });
                    loading.close();
                }
            }).catch(err => {
                ElNotification({
                    title: '出错了!',
                    message: err,
                    type: 'error'
                });
                loading.close();
            });
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
