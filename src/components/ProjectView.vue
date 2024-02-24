<template>
  <allDataWindow ref="addData" :cutid="cutid"></allDataWindow>
  <div class="InfoWrapper">
    <vidView class="compo" :cutid="cutid"></vidView>
    <MapView class="compo" ref="Map" :points="pointList"></MapView>
    <Data_Bind class="compo" ref="DataBind" :dataBind="DataBindValue" :time="TimeNow" :cutid="cutid"></Data_Bind>
    <detailedDataTable class="compo" :cutid="cutid"></detailedDataTable>
  </div>
  <div class="container">
    <div class="timeShow">当前时间：{{ TimeNow }}</div>
    <div class="timeLine">
      <TimeLine class="timeline" ref="TimeLine" :rectangles="rectangles" :TimeLineData="TimeLineData"
        @timeNow="displayTime">
      </TimeLine>
    </div>
  </div><br>
  <el-button @click="this.$refs.DataBind.print()" type="primary">Primary</el-button>
  <!-- <el-button @click="openDialog" type="primary">GetFilePath</el-button> -->
  <el-button @click="openDataDialog" type="primary">导入记录</el-button>
</template>


<script>
import TimeLine from './TimeLine.vue';
import MapView from './MapView.vue';
import allDataWindow from './all_data_window.vue'
import { socket, state } from "@/socket";
import Data_Bind from './Data_Bind.vue';
import detailedDataTable from './detailedDataTable.vue';
import vidView from './vidView.vue';

import { ref } from 'vue'

const TimeLineData = ref({})
const PointList = ref([])
const DataBindValue = ref({})

socket.on('reset_all', (data) => {
  let json = JSON.parse(data);
  TimeLineData.value = json.TimeLine;
  PointList.value = json.Map.PointsList;
  DataBindValue.value = json.DataBind;
  // this.$refs.DataBind.updateData(json.DataBind);

  console.log(json);
})
socket.on('reset_data_Bind', (data) => {
  let json = JSON.parse(data);
  DataBindValue.value = json;
  // this.$refs.DataBind.updateData(json);
  console.log(json);
})
export default {
  components: {
    TimeLine,
    MapView,
    allDataWindow,
    Data_Bind,
    detailedDataTable,
    vidView,
  },
  props: {
    cutid: {
      type: Number,
      default: -1
    }
  },
  setup() {
    return {
      TimeLineData: TimeLineData,
      pointList: PointList,
      DataBindValue: DataBindValue,
    }
  },
  data() {
    return {
      TimeNow: '',
      rectangles: [
        { x: 10, y: 20, width: 100, height: 50, color: 'blue' },
        { x: 150, y: 75, width: 200, height: 100, color: 'red' },
        { x: 400, y: 150, width: 150, height: 75, color: 'green' }
      ],
    };
  },
  methods: {
    triggerChildMethod() {
      // 使用this.$refs来访问子组件实例，并调用子组件的方法
      this.$refs.TimeLine.drawAll();
    },
    displayTime(time) {
      // console.log('displayTime', time);
      this.TimeNow = time;
    },
    openDataDialog() {
      this.$refs.addData.openDialog();
    }


  },
  mounted() {
    if (state.connected === 1) {
      socket.emit('get_all_data', { "cutid": this.$props.cutid }, (err, data) => {
        console.log(data);
        this.$refs.TimeLine.drawAll();
        this.$refs.Map.initMap();

      });

    }
  }
};
</script>


<style>
.container {
  margin: 0 0;
  padding: 0 0;

  .timeline {
    height: 200px;
    /* width: 100px; */

  }
}

.InfoWrapper {
  /* box-sizing: border-box; */

  width: calc(calc(98vw)-8px);
  padding: 0 1vw;
  /* height: 300px; */
  display: flex;
  /*超出部分换行*/
  flex-wrap: wrap;
  /* 设置高度 */
}

.compo {
  width: 50%;
  height: 35vh;
  min-height: 300px;
}
</style>



