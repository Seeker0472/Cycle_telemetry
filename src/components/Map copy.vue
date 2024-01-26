<template>
    <BMap @initd="handleInitd" :zoom="zoom">
        <BControl style="display: flex; background-color: #fff; padding: 10px" :offset="{ x: 0, y: 0 }">
            <button @click="handleZoomOut">缩小</button>
            <button @click="handleZoomIn">放大</button>
        </BControl>
    </BMap>
</template>

<!-- <script setup lang="ts">
import { ref } from 'vue'
const zoom = ref(10)
let _map
function handleInitd({ map }) {
    _map = map
}
function handleZoomOut() {
    zoom.value = _map.getZoom() - 1
}
function handleZoomIn() {
    zoom.value = _map.getZoom() + 1
}
</script> -->

<script>
let BMapGL = {};
// import { BMapGL } from 'vue3-baidu-map-gl'
export default {
    data() {
        return {
            zoom: 10
        }
    },
    created() {
        this.$nextTick(() => {
            this.createMap();
        });
    },
    props: {
        points: [],
    },
    methods: {
        createMap() {
            BMapGL = window.BMapGL;
        },
        handleInitd({ map }) {
            BMapGL = window.BMapGL;
            this._map = map;

            var polyline = new BMapGL.Polyline(this.createPointList()
                , { strokeColor: "blue", strokeWeight: 2, strokeOpacity: 0.5 });
            map.addOverlay(polyline);
        },
        handleZoomOut() {
            this.zoom = this._map.getZoom() - 1
        },
        handleZoomIn() {
            this.zoom = this._map.getZoom() + 1
        },
        createPointList() {
            let pointList = [];
            this.points.forEach(point => {
                pointList.push(new BMapGL.Point(point.lng, point.lat));
            })
            return pointList;
        }
    }
}
</script>

<style scoped>
button {
    outline: none;
    border: none;
    background: #41b883;
    margin: 0 5px;
    padding: 5px 15px;
    border-radius: 4px !important;
}

.map {
    /* display: none; */
    width: 50%;
    height: 300px;
}
</style>
