<template>
    <div>
        <el-table :data="BindInfo" height="calc(100%)">
            <el-table-column prop="name" label="名称" width="80" />
            <el-table-column label="数据源" width="180">
                <template #default="scope">
                    <el-tree-select v-model="scope.row.desc" :data="treeData" @focus="load"
                        @change="(value) => handleSelectChange(value, scope.row.id)" :props="props" style="width: 100%" />
                </template>
            </el-table-column>
            <el-table-column prop="data" label="值" />
        </el-table>
        <!-- <el-button class="mt-4" style="width: 100%; height='calc(10%)'" @click="onAddItem">Add Item</el-button> -->
    </div>
</template>

<script>
import { ref } from 'vue'
import { socket, state } from "@/socket";
const treeData = ref([]);

socket.on('reset_datasource', (data) => {
    let json = JSON.parse(data);
    // this.updateData(json)
    treeData.value = json

    console.log(json);
})

const defalutDataBind = [
    {
        'id': '0',
        'name': '时间',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '1',
        'name': '心率',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '2',
        'name': '速度',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '3',
        'name': '踏频',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '4',
        'name': '功率',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '5',
        'name': '坡度',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '6',
        'name': '温度',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '7',
        'name': '大气压',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '8',
        'name': '海拔',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '9',
        'name': '经度',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
    {
        'id': '10',
        'name': '纬度',
        'desc': 'NO DATA',
        'data': 'NULL'
    },
]
export default {
    data() {
        return {
            props: {
                label: 'name',
                value: 'file_id',
                children: 'children',
                isLeaf: 'leaf',
            },

        };
    },
    props: {
        dataBind: {
            type: Object,
        },
        cutid: {
            type: Number,
            default: -1
        },
        time: {
            type: Date,
        }
    },
    watch: {
        dataBind: {
            handler: function (data) {
                this.updateData(data);
            },
            deep: true
        }
    },
    setup() {
        const BindInfo = ref(defalutDataBind)
        return {
            BindInfo: BindInfo,
            treeData: treeData,
        }
    },
    methods: {
        load() {
            try {
                if (state.connected === 1) {
                    // 请求数据
                    let time = this.$dayjs(this.$props.time).utc().format('YYYY-MM-DDTHH:mm:ss[Z]')
                    console.log(this.$props.time, time);
                    socket.emit('get_datasource', { "cut_id": this.$props.cutid, "time": time }, (err, data) => {
                        if (err) {
                            console.error('Error:', err.message);
                            return;
                        }
                        console.log(data);
                        // this.treeData = data;
                        // console.log(this.treeData);
                    });
                }
            } catch (error) {
                console.error(error);
            }
        },


        updateData(data) {
            console.log('updateData', data);
            this.BindInfo.forEach((item) => {
                item.data = 'NULL';
                item.desc = 'NO DATA';
            })
            console.log(this.BindInfo);

            Object.entries(data).forEach(([key, value]) => {
                this.BindInfo[key].data = value.data;
                this.BindInfo[key].desc = value.file_name + '/' + value.heading_name;
            })
        },
        print() {
            console.log(this.BindInfo);
        },
        handleSelectChange(value, data_id) {
            console.log(value, data_id);
            socket.emit('bindData', { "segment_id": value.split('/')[0], "data_id": data_id, "heading_name": value.split('/')[1], "time": this.$dayjs(this.$props.time).utc().format('YYYY-MM-DDTHH:mm:ss[Z]') })
        }
    }

}

</script>