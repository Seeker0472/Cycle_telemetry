<template>
    <div id="map" class="Map"></div>
</template>

<script>
/* global BMapGL */
export default {
    name: 'HelloWorld',
    mounted() {
        // this.initMap();
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
            console.log('initMap', this.points)
            // 确保 BMapGL 全局变量可用
            if (typeof BMapGL !== 'undefined') {
                // 创建地图实例
                var map = new BMapGL.Map('map');

                Object.entries(this.points).forEach(([key, value]) => {
                    console.log(key)
                    var polyline = new BMapGL.Polyline(this.createPointList(value)
                        , { strokeColor: "blue", strokeWeight: 2, strokeOpacity: 0.5 });
                    map.addOverlay(polyline);
                })
                this.center[0] = (this.Xmin + this.Xmax) / 2;
                this.center[1] = (this.Ymin + this.Ymax) / 2;
                // 创建点坐标
                var point = new BMapGL.Point(this.center[0], this.center[1]);
                console.log(this.Xmin, this.Xmax, this.Ymin, this.Ymax);
                //设置缩放,确保整个图形都在视野中
                this.zoom = this.getZoom(this.Xmin, this.Xmax, this.Ymin, this.Ymax);

                // 初始化地图，设置中心点坐标和地图级别
                map.centerAndZoom(point, this.zoom);


            } else {
                console.error('BMapGL is not loaded');
            }
        },
        createPointList(points) {
            let pointList = [];
            this.Xmin = points[0][0];
            this.Xmax = points[0][0];
            this.Ymin = points[0][1];
            this.Ymax = points[0][1];
            points.forEach(point => {
                pointList.push(new BMapGL.Point(point[0], point[1]));
                if (point[0] < this.Xmin) {
                    this.Xmin = point[0];
                }
                if (point[0] > this.Xmax) {
                    this.Xmax = point[0];
                }
                if (point[1] < this.Ymin) {
                    this.Ymin = point[1];
                }
                if (point[1] > this.Ymax) {
                    this.Ymax = point[1];
                }
            })

            return pointList;
        },
        getZoom(Xmin, Xmax, Ymin, Ymax) {
            Xmax - Xmin;
            Ymax - Ymin;
            return 10;
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
