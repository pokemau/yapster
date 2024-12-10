const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/${currentChatID}/`;
// Create a new WebSocket connection
export const socket = new WebSocket(wsEndpoint);
// Successful connection event
socket.onopen = (event) => {
    console.log("WebSocket connection openeddddd!");
};
// Socket disconnect event
socket.onclose = (event) => {
    console.log("WebSocket connection closed!");
};
