let socket = null;

export const connectWebSocket = (userId, onMessage) => {
  if (socket) return;

  socket = new WebSocket(`ws://127.0.0.1:8000/ws/${userId}`);

  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  socket.onmessage = (event) => {
    // Backend sends plain text
    onMessage(event.data);
  };

  socket.onclose = () => {
    console.log("WebSocket disconnected");
    socket = null;
  };

  socket.onerror = (error) => {
    console.error("WebSocket error", error);
  };
};

export const disconnectWebSocket = () => {
  if (socket) {
    socket.close();
    socket = null;
  }
};
