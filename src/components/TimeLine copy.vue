<template>
    <canvas ref="TimeLine" id="canvas" class="timeline" @mousedown="startDrag" @mousemove="onDrag" @mouseup="endDrag">

    </canvas>
    <!-- <div>111</div> -->
</template>
<script>
export default {
    data() {
        return {
            scale: 30,
            begin: 0,
            end: 0,
            length: 0,
            begin: 0
        };
    },
    name: 'TimeLine',
    // data() {
    //     return {
    //         // 在这里添加你的数据

    //     };
    // },
    props: {
        timelineEvents: [],
        rectangles: [],
    },
    mounted() {
        // console.log('123');
        // console.log(this.rectangles);
        // let utcTime = '2024-01-22T12:00:00Z';
        // console.log(this.$dayjs(utcTime).toDate());
        // console.log(this.$dayjs('2024-01-22T12:00:00Z').isSameOrAfter('2010-10-19'));
        this.drawAll();
    },

    methods: {
        drawAll() {
            this.setWidthHeight();
            window.addEventListener('resize', this.setWidthHeight);
            this.drawTimeLine(0);
        },
        getFirstLast() {
            let first = this.timelineEvents[0].timestart;
            let last = this.timelineEvents[0].timeend;
            let length = 0;
            this.timelineEvents.forEach(element => {
                if (this.$dayjs(element.timestart).isBefore(first)) {
                    first = element.timestart;
                }
                if (this.$dayjs(element.timeend).isAfter(last)) {
                    last = element.timeend;
                }
            });
            this.begin = first;
            this.end = last;
            this.length = length = this.$dayjs(last).diff(this.$dayjs(first), 'minute');
            // console.log(first, last, length);
            return [first, last];
        },

        drawTimeLine(begin = 0) {
            // begin = begin - begin % 30;
            this.getFirstLast();
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "rgb(40,40,40)";
            ctx.fillRect(0, 0, canvas.width, canvas.height / 10);

            console.log(this.length);
            for (let i = 0; i <= this.length; i += 30) {
                ctx.beginPath();
                this.drawLine((i - begin) * this.scale, 0, (i - begin) * this.scale, canvas.height / 10, 1, '#fff');
                // if (scale >= 2) {
                ctx.font = "10px Arial";
                ctx.fillStyle = "#fff";
                ctx.fillText(i, (i - begin) * this.scale, canvas.height / 10);
                if (this.scale >= 2) {
                    this.drawLine(((i - begin) + 15) * this.scale, 0, ((i - begin) + 15) * this.scale, canvas.height / 15, 1, '#fff');
                    if (this.scale >= 5) {
                        for (let j = 1; j < 10; j++) {
                            if (j === 5) {
                                continue;
                            }
                            this.drawLine(((i - begin) + 3 * j) * this.scale, 0, ((i - begin) + 3 * j) * this.scale, canvas.height / 20, 1, '#fff');
                        }
                    }
                }
            }
        },
        drawObjectParent() {
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");
            this.rectangles.forEach(element => {
                ctx.fillStyle = element.color;
                ctx.fillRect(element.x, element.y, element.width, element.height);
            });
        },
        draw() {
            this.setWidthHeight();
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");
            ctx.fillStyle = "rgb(200,0,0)";
            ctx.fillRect(20, 20, 150, 100);
            this.drawLine(0, 0, 100, 100);
            this.drawObjectParent();

            // 当用户滚动鼠标滚轮时进行缩放
            canvas.addEventListener('wheel', (evt) => {
                var mousex = evt.clientX - canvas.offsetLeft;
                var mousey = evt.clientY - canvas.offsetTop;
                var wheel = evt.deltaY < 0 ? 1 : -1;

                console.log(mousex, mousey, wheel);
                // 计算缩放值
                var zoom = Math.exp(wheel * 0.01);
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                // 缩放绘图内容
                ctx.translate(mousex, 1);
                ctx.scale(zoom, 1);
                ctx.translate(-mousex, -1);
                this.drawObjectParent();
                evt.preventDefault();
            }, false);
        },
        setWidthHeight() {
            var canvas = document.getElementById("canvas");
            var context = canvas.getContext("2d");
            // canvas.width = window.innerWidth;
            // canvas.height = window.innerHeight;
            // console.log(canvas.width, canvas.height);
            const element = this.$refs.TimeLine;
            const width = element.offsetWidth;
            const height = element.offsetHeight;
            var getPixelRatio = function (context) {
                var backingStore = context.backingStorePixelRatio ||
                    context.webkitBackingStorePixelRatio ||
                    context.mozBackingStorePixelRatio ||
                    context.msBackingStorePixelRatio ||
                    context.oBackingStorePixelRatio ||
                    context.backingStorePixelRatio || 1;
                return (window.devicePixelRatio || 1) / backingStore;
            };
            var ratio = getPixelRatio(context);
            canvas.width = width * ratio;
            canvas.height = height * ratio;
            console.log(`Width: ${width}, Height: ${height}`);
        },
        drawLine(x1, y1, x2, y2, lineWidth = 1, color = '#fff') {
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.lineWidth = lineWidth;
            ctx.strokeStyle = color;
            ctx.stroke();
        },
        // 在这里添加你的方法
    },

    // 在这里添加你的生命周期钩子
};
</script>

<style scoped>
.timeline {
    background-color: rgb(30, 44, 44);
    width: calc(100%);
    height: 100%;
    /* 在这里添加你的 CSS 样式 */
}
</style>

<!-- /* 在 Vue.js 中，:initTime="time3" 和 @timeChange="timeChange3" 是父子组件之间通信的两种方式。

:initTime="time3"：这是父组件向子组件传递数据的方式。在这里，initTime 是子组件 TimeLine 的一个 prop，父组件通过 :initTime 向子组件传递了一个名为 time3 的数据。子组件可以通过 this.initTime 来访问这个数据。注意，这里的 : 是 v-bind 的简写，用于绑定父组件的数据到子组件的 prop。

@timeChange="timeChange3"：这是子组件向父组件发送消息的方式。在这里，timeChange 是子组件 TimeLine 触发的一个自定义事件，父组件通过 @timeChange 监听这个事件，并指定当事件触发时执行一个名为 timeChange3 的方法。注意，这里的 @ 是 v-on 的简写，用于监听子组件的事件。

所以，如果你想在 TimeLine 组件中使用 initTime prop 和 timeChange 事件，你需要在 TimeLine 组件的选项中定义它们：

在这个例子中，我们在 mounted 生命周期钩子中触发了 timeChange 事件。你可以根据你的需求在合适的地方触发这个事件。*/ -->