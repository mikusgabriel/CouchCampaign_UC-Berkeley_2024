using MikeSchweitzer.WebSocket;
using System;

public class ServerConnection : MonoBehaviour
{
    private WebSocketConnection websocket;

    private void Start()
    {
        websocket.StateChanged += OnStateChanged;
        websocket.Connect("ws://localhost:8000/ws/unity");
    }

    private void OnDestroy()
    {
        websocket.StateChanged -= OnStateChanged;
        websocket.Disconnect();
    }

    void Update()
    {
        while (websocket.TryRemoveIncomingMessage(out string message))
        {
            var json = JsonUtility.FromJson<JsonData>(message);

            //Do something here...
        }
    }



    private void OnStateChanged(WebSocketConnection connection, WebSocketState oldState, WebSocketState newState)
    {

        if (newState == WebSocketState.Connected)
        {
            Debug.Log("Server Connected");
        }
        else if (newState == WebSocketState.Disconnected)
        {
            Debug.Log("Server Disconnected");
            websocket.Connect();
        }
    }

    [Serializable]
    private class JsonData
    {
        public string type;
    }
}
