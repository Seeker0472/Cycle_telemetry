<template>
    <el-dialog v-model="centerDialogVisible" title="添加账号" width="500" align-center>
        <span>平台:</span>
        <div>
            <el-radio-group v-model="Platform" size="default">
                <el-radio-button label="Xingzhe" />
                <el-radio-button label="XOSS" />
                <el-radio-button label="Strava" />
                <el-radio-button label="Garmin" />
            </el-radio-group>
        </div>
        <span>账号:</span>
        <el-input v-model="account" placeholder="账号" />
        <span>密码:</span>
        <el-input v-model="passWord" type="password" show-password placeholder="密码" />

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
        const Platform = ref('Xingzhe')
        const centerDialogVisible = ref(false)
        const passWord = ref('')
        const account = ref('')
        return {
            Platform,
            centerDialogVisible,
            passWord,
            account
        }
    },
    methods: {
        showWindow() {
            this.centerDialogVisible = true;
        },
        proceed() {
            let data = {
                Platform: this.Platform,
                account: this.account,
                passWord: this.passWord
            }
            switch (this.Platform) {
                case 'Xingzhe':
                    data.Platform = 1;
                    break;
                case 'XOSS':
                    data.Platform = 2;
                    break;
                case 'Strava':
                    data.Platform = 3;
                    break;
                case 'Garmin':
                    data.Platform = 4;
                    break;
                default:
                    ElNotification({
                        title: '失败',
                        message: '未知平台' + this.Platform,
                        type: 'error'
                    });

                    return;
            }
            if (data.Platform != 1) {
                ElNotification({
                    title: '失败',
                    message: '暂时只支持行者国内版',
                    type: 'error'
                });
                return;
            }
            if (this.account == '' || this.passWord == '') {
                ElNotification({
                    title: '错误',
                    message: '账号或密码不能为空',
                    type: 'error'
                });
                return;
            }

            const loading = ElLoading.service({
                lock: true,
                text: '请稍后...',
                background: 'rgba(0, 0, 0, 0.7)',
            })
            this.$axios.post('/api/addAccount', data).then(response => {
                if (response.data.stat == 'OK') {
                    ElNotification({
                        title: '成功',
                        message: '添加成功',
                        type: 'success'
                    });
                    this.centerDialogVisible = false;
                } else {
                    ElNotification({
                        title: '失败',
                        message: response.data.msg,
                        type: 'error'
                    });
                }
            }).catch(error => {
                ElNotification({
                    title: '失败',
                    message: error,
                    type: 'error'
                });
            });
            loading.close()
        },
    }
}



</script>