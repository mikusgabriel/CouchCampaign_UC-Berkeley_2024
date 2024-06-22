using MikeSchweitzer.WebSocket;
using System;
using System.Threading.Tasks;
using UnityEngine;


public class ServerConnection : MonoBehaviour
{

    [SerializeField]
    private WebSocketConnection websocket;


    [SerializeField]
    private GameObject characterPrefab;



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

            OnMessageReceived(json.type,message);
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


    //Dunno why there is an error here
    async void OnMessageReceived(string type, string message)
    {
        Debug.Log(message);

        switch (type)
        {
            case "type":
                {
                    Debug.Log("here?"); break;
                }


        }
    }



    public void SendJson(object obj)
    {
        var message = JsonUtility.ToJson(obj);
        SendString(message);
    }


    public void SendString(string message)
    {
        websocket.AddOutgoingMessage(message);
    }


    [Serializable]
    private class JsonData
    {
        public string type;
    }
}
