<template>
    <canvas ref="TimeLine" id="canvas" class="timeline" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp"
        @mouseleave="mouseLeave" @touchstart="touchStart" @touchmove="touchMove" @touchend="touchEnd"
        @touchcancel="mouseLeave">

    </canvas>
    <!-- <div>111</div> -->
</template>
<script>
export default {
    data() {
        return {
            scale: 30000,
            length: 0,
            begin: 0,
            end: 0,
            pivot: 0,
            offsetMilliSec: 0,
            drag: 0,
            offSetY: 0,
            screenPixelRatio: 1,
            EntryExitMilliSec: [0, 1],
        };
    },
    name: 'TimeLine',
    props: {
        TimeLineData: {},
        rectangles: [],
    },
    mounted() {
        //延时绘制
        // setTimeout(() => {
        //     this.drawAll();
        // }, 1);
        // this.drawAll();
    },

    methods: {
        //TODO:适配移动端
        touchStart(event) {
            console.log(event);
        },
        touchMove(event) {
            console.log(event);
        },
        touchEnd(event) {
            console.log(event);
        },

        drawAll() {//画出所有东西
            this.$emit('timeNow', this.$dayjs(this.begin).add(this.offsetMilliSec, 'millisecond').toDate());
            this.setWidthHeight();
            window.addEventListener('resize', this.drawAll);
            this.drawTimeLine(this.offsetMilliSec, this.pivot);
            this.drawEntryExitPoint();
        },
        mouseLeave() {
            this.drag = 0;
        },
        mouseDown(evt) {
            const canvas = document.getElementById("canvas");
            // let x = evt.offsetX * this.screenPixelRatio;
            // let y = evt.offsetY * this.screenPixelRatio;
            let x = evt.offsetX;
            let y = evt.offsetY;
            //点击左上角,暂时什么都不做
            // if ((y < canvas.height / 10) && (x < 40)) {
            //     console.log("click on TopLeft");
            // }
            // //点击了最上面的时间,需要判断位置,设置drag为不同的值
            // else
            if (y < canvas.height / 10) {
                // console.log("x=" + x + "pivot=" + this.pivot);
                if (x > this.pivot - 10 + 40 && x < this.pivot + 10 + 40) {

                    //点击了时间线,设置drag
                    this.drag = 2;
                }
                else {
                    //点击了其他地方,设置drag
                    this.drag = 1;
                }
                console.log("click on Top");
            }
            //点击了左边的时间轴序号,设置drag
            else if (x < 40) {
                this.drag = 3;
                console.log("click on Left");
            }
            //点击了时间轴,暂时什么都不做
            else {
                console.log("click on TimeLine");
            }
        },
        mouseMove(evt) {
            let x = evt.offsetX;
            // let y = evt.offsetY;
            // console.log(evt.movementX, evt.offsetX);
            // let px = x - this.mousePos[0];
            if (this.drag != 0) {
                switch (this.drag) {
                    case 1:
                        //拖动时间轴
                        this.moveTimeLine(evt.movementX);
                        // this.jumpToTargetPivot(this.pivot + x - this.mousePos[0]);
                        break;
                    case 2:
                        //拖动时间线
                        this.jumpToTargetPivot(x - 40);
                        console.log("drag timeLine" + x);
                        break;
                    case 3:
                        //拖动左边的时间轴序号
                        this.moveTimeLineUpDown(evt.movementY);
                        break;
                }
                // this.mousePos = [evt.clientX, evt.clientY];
                console.log("mousemove" + this.mousePos);
                // this.jumpToTargetPivot(this.pivot + this.mousePos[0] - this.mousePos[0]);
            }
        },
        mouseUp(evt) {
            this.drag = 0;
            this.mousePos = [evt.clientX, evt.clientY];
            // console.log("mouseup" + this.mousePos);
        },
        moveTimeLineUpDown(deltaY) {
            if (this.offSetY + deltaY < 0)
                this.offSetY += deltaY;
            else
                this.offSetY = 0;
            this.drawAll();
        },
        //获取第一个和最后一个时间和持续时间长度(分钟)
        getFirstLast() {
            console.log(this.TimeLineData);
            let first = this.TimeLineData.segments[0].time_start;
            let last = this.TimeLineData.segments[0].time_end;
            let length = 0;
            this.TimeLineData.segments.forEach(element => {
                if (this.$dayjs(element.time_start).isBefore(first)) {
                    first = element.time_start;
                }
                if (this.$dayjs(element.time_end).isAfter(last)) {
                    last = element.time_end;
                }
            });
            //取整点(开始向下取整,结束向上取整)
            this.begin = this.$dayjs(first).startOf('hour');
            // 如果当前时间不是整点，则加上足够的分钟数达到下一个整点
            last = this.$dayjs(last);
            if (last.minute() !== 0 || last.second() !== 0 || last.millisecond() !== 0) {
                last = last.add(1, 'hour').startOf('hour');
            }
            this.end = last;
            console.log(this.begin.toDate(), this.end.toDate(), this.end.diff(this.begin));
            //以毫秒为单位
            this.length = length = this.end.diff(this.begin);
            this.EntryExitMilliSec[1] = length;
            // console.log(first, last, length);
            return [first, last];
        },
        //画出时间轴
        drawTimeLine(offsetSec = 0, pivot = 0) {
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");

            ctx.scale(this.screenPixelRatio, this.screenPixelRatio);

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            this.drawTimeLineContainer();

            pivot += 40;
            // begin = begin - begin % 30;
            this.getFirstLast();

            ctx.fillStyle = "rgb(40,40,40)";
            ctx.fillRect(0, 0, canvas.width, canvas.height / 10);

            console.log(this.length);
            for (let i = 0; i <= this.length; i += 60000 * 30) {//每30分钟循环一次
                ctx.beginPath();
                this.drawLine((i - offsetSec) / this.scale + pivot, 0, (i - offsetSec) / this.scale + pivot, canvas.height / 10, 1, '#fff');
                // if (scale >= 2) {
                ctx.font = "10px Arial";
                ctx.fillStyle = "#fff";
                //有问题!!!!
                ctx.fillText((this.$dayjs(this.begin).add(i / 60000, 'minute')).format('D-h:mm'), (i - offsetSec) / this.scale + pivot, canvas.height / 11);
                if (this.scale <= 200000) {
                    this.drawLine(((i - offsetSec) + 15 * 60000) / this.scale + pivot, 0, ((i - offsetSec) + 15 * 60000) / this.scale + pivot, canvas.height / 15, 1, '#fff');
                    if (this.scale <= 20000) {
                        for (let j = 1; j < 10; j++) {
                            if (j === 5) {
                                continue;
                            }
                            this.drawLine(((i - offsetSec) + 3 * j * 60000) / this.scale + pivot, 0, ((i - offsetSec) + 3 * j * 60000) / this.scale + pivot, canvas.height / 20, 1, '#fff');
                        }
                    }
                }
            }
            this.drawTimeLineObject();

            //画出当前时间线
            this.drawLine(pivot, 0, pivot, canvas.height, 1, '#fff');
            ctx.beginPath();
            ctx.moveTo(pivot, canvas.height / 30);
            ctx.lineTo(pivot + 10, 0);
            ctx.lineTo(pivot - 10, 0);
            ctx.fillStyle = "#fff";
            ctx.fill();
        },
        //画出时间轴容器
        drawTimeLineContainer(times = 3) {
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");

            ctx.fillStyle = "rgb(40,40,40)";
            ctx.fillRect(0, canvas.height / 10, 40, canvas.height);
            for (let i = 0; i < times + 1; i++) {
                // ctx.fillRect(40+this.scale*60*i, canvas.height / 10, 60*this.scale, canvas.height);
                this.drawLine(0, canvas.height / 10 * (i + 1) + this.offSetY, canvas.width, canvas.height / 10 * (i + 1) + this.offSetY, 1, '#fff');
            }
            for (let i = 0; i < times; i++) {
                ctx.font = "25px Arial";
                ctx.fillStyle = "#fff";
                ctx.fillText(i + 1, 15, canvas.height / 10 * (i + 2) - canvas.height / 35 + this.offSetY);
            }
            this.drawLine(40, 0, 40, canvas.height, 1, '#fff');
        },
        //跳转到指定时间
        jumpToTargetSec(targetSec) {
            this.pivot = this.pivot + (targetSec - this.offsetMilliSec) * this.scale;

            this.offsetMilliSec = targetSec;

            this.drawAll();
        },
        //跳转到指定偏移量TODO:要修改!!!!
        jumpToTargetPivot(targetPivot) {
            this.offsetMilliSec = this.offsetMilliSec + (targetPivot - this.pivot) * this.scale;

            this.pivot = targetPivot;

            this.drawAll();
        },
        moveTimeLine(px) {
            if (this.pivot <= 0 && px < 0) {
                // this.pivot = 0;
                this.offsetMilliSec -= px * this.scale;
                console.log("offsetMilliSec" + this.offsetMilliSec);
            } else {
                this.pivot += px;
            }
            // this.offsetSec += px / this.scale;
            this.drawAll();
        },
        drawTimeLineObject() {
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");

            this.TimeLineData.segments.forEach(element => {
                ctx.fillStyle = "rgb(200,0,0)";
                // console.log((this.$dayjs(element.time_start).diff(this.begin) - this.offsetMilliSec) / this.scale + this.pivot, canvas.height / 10 * element.line + 2);
                ctx.fillRect((this.$dayjs(element.time_start).diff(this.begin) - this.offsetMilliSec) / this.scale + this.pivot, canvas.height / 10 * element.row_id + 2, this.$dayjs(element.time_end).diff(element.time_start) / this.scale, canvas.height / 11);
                console.log("scale" + this.scale + "offsetMilliSec" + this.offsetMilliSec + "pivot" + this.pivot + "start" + (this.$dayjs(element.time_start).diff(this.begin) - this.offsetMilliSec) / this.scale + this.pivot + "end" + (this.$dayjs(element.time_end).diff(this.begin) - this.offsetMilliSec) / this.scale + this.pivot);
            });

        },
        drawEntryExitPoint() {
            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");
            let startpx = (this.EntryExitMilliSec[0] - this.offsetMilliSec) / this.scale + this.pivot + 40;
            let endpx = (this.EntryExitMilliSec[1] - this.offsetMilliSec) / this.scale + this.pivot + 40;
            ctx.fillStyle = "rgb(40,40,40)";
            console.log("ca" + canvas.height);
            ctx.fillRect(0, canvas.height / this.screenPixelRatio * 9 / 10, canvas.width, canvas.height / this.screenPixelRatio / 10);
            ctx.fillStyle = "rgb(230, 230, 230)";
            ctx.fillRect(startpx, canvas.height / this.screenPixelRatio * 9 / 10, endpx - startpx, canvas.height / this.screenPixelRatio / 10);
            ctx.fillStyle = "rgb(200,0,0)";
            ctx.fillRect(startpx, canvas.height / this.screenPixelRatio * 9 / 10, 5, canvas.height / this.screenPixelRatio / 10);
            ctx.fillRect(endpx - 5, canvas.height / this.screenPixelRatio * 9 / 10, 5, canvas.height / this.screenPixelRatio / 10);

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
            this.jumpToTargetPivot(100);
            this.drawTimeLineObject();
        },
        //设置画布宽高
        setWidthHeight() {
            var canvas = document.getElementById("canvas");
            var context = canvas.getContext("2d");
            // canvas.width = window.innerWidth;
            // canvas.height = window.innerHeight;
            // console.log(canvas.width, canvas.height);
            const element = this.$refs.TimeLine;
            if (!element) {
                console.log('element is null');
                // window.setTimeout(this.drawAll, 500);
                return;
            }
            console.log(element);
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
            this.screenPixelRatio = ratio;
            // canvas.width = width * ratio;
            // canvas.height = height * ratio;
            canvas.width = width * ratio;
            canvas.height = height * ratio;
            canvas.style.height = '200px';
            canvas.style.width = '100%';
            console.log(`Width: ${width}, Height: ${height}, Ratio: ${ratio}`);
            //延时绘制
            // setTimeout(() => {
            //     this.drawAll();
            // }, 1);
        },
        //画线
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