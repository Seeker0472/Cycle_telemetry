import { reactive } from "vue";
import { io } from "socket.io-client";

export const state = reactive({
    connected: -1,
    fooEvents: [],
    barEvents: []
});

const URL = "http://localhost:5000/test";

export const socket = io(URL);

socket.on("connect", () => {
    state.connected = 1;
    console.log("connect")
});

socket.on("disconnect", () => {
    state.connected = 0;
    console.log("disconnect")
});

socket.on("foo", (...args) => {
    state.fooEvents.push(args);
});

socket.on("bar", (...args) => {
    state.barEvents.push(args);
});