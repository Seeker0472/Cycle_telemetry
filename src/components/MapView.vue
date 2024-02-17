<template>
    <div id="map" class="Map"></div>
</template>

<script>
/* global BMapGL */
export default {
    name: 'HelloWorld',
    mounted() {
        this.initMap();
    },
    data() {
        return {
            zoom: 10,
            center: [116.404, 39.915],
        }
    },
    props: {
        points: [],
    },
    methods: {
        initMap() {
            // 确保 BMapGL 全局变量可用
            if (typeof BMapGL !== 'undefined') {
                // 创建地图实例
                var map = new BMapGL.Map('map');
                // 创建点坐标
                var point = new BMapGL.Point(this.center[0], this.center[1]);
                var polyline = new BMapGL.Polyline(this.createPointList()
                    , { strokeColor: "blue", strokeWeight: 2, strokeOpacity: 0.5 });
                map.addOverlay(polyline);
                // 初始化地图，设置中心点坐标和地图级别
                map.centerAndZoom(point, this.zoom);


            } else {
                console.error('BMapGL is not loaded');
            }
        },
        createPointList() {
            let pointList = [];
            let Xmin = this.points[0].lng;
            let Xmax = this.points[0].lng;
            let Ymin = this.points[0].lat;
            let Ymax = this.points[0].lat;
            this.points.forEach(point => {
                pointList.push(new BMapGL.Point(point.lng, point.lat));
                if (point.lng < Xmin) {
                    Xmin = point.lng;
                }
                if (point.lng > Xmax) {
                    Xmax = point.lng;
                }
                if (point.lat < Ymin) {
                    Ymin = point.lat;
                }
                if (point.lat > Ymax) {
                    Ymax = point.lat;
                }
            })
            this.center[0] = (Xmin + Xmax) / 2;
            this.center[1] = (Ymin + Ymax) / 2;
            //设置缩放,确保整个图形都在视野中
            this.zoom = this.getZoom(Xmin, Xmax, Ymin, Ymax);
            return pointList;
        },
        getZoom(Xmin, Xmax, Ymin, Ymax) {
            Xmax - Xmin;
            Ymax - Ymin;
            return 15;
        }
    }
};
</script>

<style scoped>
.Map {
    min-width: 40vw;
    min-height: 300px;

}
</style>
