using MikeSchweitzer.WebSocket;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ServerConnection : MonoBehaviour
{
    private WebSocketConnection websocket;

    private void Start()
    {
        websocket = new WebSocketConnection();
        websocket.Connect("wss://ws.postman-echo.com/raw");
    }

}
