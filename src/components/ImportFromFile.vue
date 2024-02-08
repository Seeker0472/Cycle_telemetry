<template>
    <el-dialog v-model="centerDialogVisible" title="请确认详细信息" width="500" align-center>
        <span>文件路径:</span>
        <el-input v-model="input" placeholder="文件路径">
            <template #append>
                <el-button @click="selectFile">
                    <el-icon>
                        <FolderOpened />
                    </el-icon>
                </el-button>
            </template>
        </el-input>
        <span>文件类型:</span>
        <div>
            <el-radio-group v-model="FileType" size="default">
                <el-radio-button label="FIT" />
                <el-radio-button label="GPX" />
                <el-radio-button label="MP4" />
                <el-radio-button label="CSV" />
            </el-radio-group>
        </div>
        <span>名字:</span>
        <el-input v-model="name" placeholder="名字" />
        <span>描述:</span>
        <el-input v-model="description" placeholder="描述" />

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
        const input = ref('')
        const name = ref('')
        const description = ref('')
        const centerDialogVisible = ref(false)
        const FileType = ref('FIT')
        return {
            input,
            name,
            description,
            centerDialogVisible,
            FileType
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
            window.electronAPI.send('open-file-dialog');
        },
        selectFile() {
            window.electronAPI.send('open-file-dialog');
        },
        processFileName() {
            // console.log(this.input);
            let name = this.input.split('\\').pop().split('/').pop();
            this.name = name;
            let type = name.split('.').pop().toUpperCase();
            this.FileType = type;
            if (!(['FIT', 'GPX', 'MP4', 'CSV'].includes(type.toUpperCase()))) {
                ElNotification({
                    title: 'Warning!',
                    message: '似乎导入了一个不受支持的文件, 请检查文件是否正确或者手动选择文件类型',
                    type: 'warning',
                    duration: 10000,
                })
            }
        },
        proceed() {
            if (this.input == '') {
                ElNotification({
                    title: '文件路径不能为空!',
                    message: '请选择文件',
                    type: 'error',
                })
                return
            }
            if (this.name == '') {
                ElNotification({
                    title: '名字不能为空!',
                    message: '请输入名字或者重新选择文件',
                    type: 'error',
                })
                return
            }
            if (!(['FIT', 'GPX', 'MP4', 'CSV'].includes(this.FileType.toUpperCase()))) {
                ElNotification({
                    title: '请选择文件类型!',
                    message: '我们无法自动判断你选择文件的类型,请注意:目前我们的软件只支持FIT, GPX, MP4, CSV文件, 如果你坚信你没有选错文件,请手动选择文件类型',
                    type: 'error',
                    duration: 17000,
                })
                return
            }
            const loading = ElLoading.service({
                lock: true,
                text: '正在读取文件,请稍后...',
                background: 'rgba(0, 0, 0, 0.7)',
            })
            this.$axios.post('/api/addFile', {
                name: this.name,
                description: this.description,
                type: this.FileType,
                path: this.input
            })
                .then((response) => {
                    if (response.data.stat == 'OK') {
                        ElNotification({
                            title: '导入成功!',
                            message: '文件已经成功导入',
                            type: 'success',
                        })
                        loading.close()
                        this.centerDialogVisible = false;
                        this.reset()
                    } else {
                        ElNotification({
                            title: '导入失败!',
                            message: response.data.msg,
                            type: 'error',
                        })
                        loading.close()
                    }
                }).catch((error) => {
                    console.log(error);
                    ElNotification({
                        title: '出错了!',
                        message: error,
                        type: 'error',
                    })
                    loading.close()
                })

        },
        reset() {
            this.input = '';
            this.name = '';
            this.description = '';
            this.FileType = 'FIT';
        }

    },
    mounted() {
        window.electronAPI.receive('selected-file', (filePaths) => {
            this.input = filePaths[0];
            this.processFileName();
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
</style>
