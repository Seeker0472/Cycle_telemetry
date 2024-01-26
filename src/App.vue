<template>
  <div class="vidAndMap">
    <img class="vid" src="./assets/pic.png" alt="">
    <!-- <img class="map" src="./assets/pic.png" alt=""> -->
    <MapView class="map" ref="Map" :points="pointList"></MapView>
  </div>
  <br>
  <div class="container">
    <div class="timeShow">当前时间：{{ showTime3 }}</div>
    <div class="timeLine">
      <!-- <TimeLine ref="TimeLine" :initTime="time3" @timeChange="timeChange3" :timeSegments="timeSegments3"
        @click_timeSegments="click_timeSegments3" :windowList="windowList"
        @click_window_timeSegments="click_window_timeSegments"></TimeLine> -->
      <TimeLine ref="TimeLine" :rectangles="rectangles" :timelineEvents="timelineEvents" @timeNow="displayTime">
      </TimeLine>
    </div>
  </div><br>
  <!-- <el-button @click="triggerChildMethod" type="primary">Primary</el-button> -->
</template>


<script>
import TimeLine from './components/TimeLine.vue';
import MapView from './components/MapView.vue';
export default {
  components: {
    TimeLine,
    MapView
  },
  // 其他选项...
  data() {
    return {
      showTime3: '12',
      timelineEvents: [
        {
          id: 1,
          title: "Event 1",
          line: 1,
          timestart: "2024-01-13T05:39:30.100Z",
          timeend: "2024-01-13T05:50:30.000Z",
          description: "Description of event 1"
        },
        {
          id: 2,
          title: "Event 2",
          line: 1,
          timestart: "2024-01-13T06:39:30.000Z",
          timeend: "2024-01-13T06:50:30.000Z",
          description: "Description of event 2"
        },
        {
          id: 3,
          title: "Event 3",
          line: 1,
          timestart: "2024-01-13T07:39:30.000Z",
          timeend: "2024-01-13T07:50:30.000Z",
          description: "Description of event 3"
        },
        {
          id: 4,
          title: "Event 4",
          line: 1,
          timestart: "2024-01-13T08:39:30.000Z",
          timeend: "2024-01-13T08:50:30.000Z",
          description: "Description of event 4"
        },
        {
          id: 5,
          title: "Event 5",
          line: 1,
          timestart: "2024-01-13T09:39:30.000Z",
          timeend: "2024-01-13T09:50:30.000Z",
          description: "Description of event 5"
        },
        {
          id: 6,
          title: "Event 6",
          line: 1,
          timestart: "2024-01-13T10:39:30.000Z",
          timeend: "2024-01-13T10:50:30.000Z",
          description: "Description of event 6"
        },
        {
          id: 7,
          title: "Event 7",
          line: 1,
          timestart: "2024-01-13T11:39:30.000Z",
          timeend: "2024-01-13T11:50:30.000Z",
          description: "Description of event 7"
        },
        {
          id: 8,
          title: "Event 8",
          line: 1,
          timestart: "2024-01-13T12:39:30.000Z",
          timeend: "2024-01-13T12:50:30.000Z",
          description: "Description of event 8"
        }
      ],
      rectangles: [
        { x: 10, y: 20, width: 100, height: 50, color: 'blue' },
        { x: 150, y: 75, width: 200, height: 100, color: 'red' },
        { x: 400, y: 150, width: 150, height: 75, color: 'green' }
      ],
      pointList: [
        { lng: 116.399, lat: 39.910 },
        { lng: 116.405, lat: 39.920 },
        { lng: 116.425, lat: 39.900 }
      ],
    };
  },
  methods: {
    triggerChildMethod() {
      // alert("success");
      // 使用this.$refs来访问子组件实例，并调用子组件的方法
      this.$refs.TimeLine.draw();
      // window.addEventListener('resize', this.$refs.TimeLine.setWidthHeight);
    },
    displayTime(time) {
      this.showTime3 = time;
    },
    // mounted() {
    //   alert("success");
    //   this.$refs.TimeLine.draw(); // Call the desired function here
    //   window.addEventListener('resize', this.$refs.TimeLine.setWidthHeight);
    // },


  }
};
</script>

<style>
.container {
  width: calc(96vw);
  /* 或者 width: 100%; */
  height: 100%;
  margin: 0 0;
  padding: 0 0;
  /* display: block; */
  /* position: relative; */
  /* justify-content: center; */
  /* flex-direction: column; */

  .timeLine {
    height: 200px;

  }
}

.vidAndMap {
  box-sizing: border-box;
  height: 300px;
  /* 设置高度 */
}

.vid {
  width: 50%;
  height: inherit;
  /* 设置高度 */
  float: left;
}

.map {
  position: relative;
  width: 50%;
  height: inherit;
  /* 设置高度 */
  float: right;
}

#app {
  max-width: 100%;
  margin: 0 auto;
  padding: 0vw;
}
</style>
