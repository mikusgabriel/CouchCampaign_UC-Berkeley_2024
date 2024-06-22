using MikeSchweitzer.WebSocket;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ServerConnection : MonoBehaviour
{
    public class Tester : MonoBehaviour
    {
        public WebSocketConnection _Connection;
        public string _Url = "wss://ws.postman-echo.com/raw";
    }
}
