using MikeSchweitzer.WebSocket;
using System;
using UnityEngine;
using System.Text;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using UnityEngine.TextCore.Text;



public class ServerConnection : MonoBehaviour
{
    [SerializeField]
    private WebSocketConnection websocket;
    [SerializeField]
    private CameraManager cameraManager;
    [SerializeField]
    private Camera cam;
    [SerializeField]
    private MapRenderer mapRenderer;

    [Header("Things")]
    [SerializeField]
    private TextToSpeech textToSpeech;
    [SerializeField]
    private MusicPlayer musicPlayer;
    [SerializeField]
    private DiceSpawner diceSpawner;



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
            print(message);
            var json = JsonUtility.FromJson<JsonData>(message);

            OnMessageReceived(json.type, message);
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


    async void OnMessageReceived(string type, string message)
    {
        Debug.Log(message);

        switch (type)
        {
            case "map":
                {
                    var data = JsonUtility.FromJson<MapJsonData>(message);

                    byte[] byteArray = Convert.FromBase64String(data.map);
                    mapRenderer.LoadMapFromFile(byteArray);
                    mapRenderer.SetTerrainHeight();

                    bool go = true;
                    foreach (Entity entity in data.entities)
                    {
                        Transform tr = transform.Find(entity.name);

                        if (tr != null)
                        {
                            tr.position = mapRenderer.GetWorldPosition(entity.x, entity.y);

                            if (go)
                            {
                                go = false;
                                cameraManager.Follow(tr.gameObject);
                                await Task.Delay(500);
                                cameraManager.SetZoomLevel(1.5f);
                            }
                            continue;
                        }

                        GameObject playerObject = Instantiate(characterPrefab, mapRenderer.GetWorldPosition(entity.x, entity.y), Quaternion.identity, transform);
                        playerObject.name = entity.name;

                        UseMeshyMesh script = playerObject.GetComponent<UseMeshyMesh>();
                        script.SetMesh(entity.meshyId);

                        if (go)
                        {
                            go = false;
                            cameraManager.Follow(playerObject);
                            await Task.Delay(500);
                            cameraManager.SetZoomLevel(1.5f);
                        }
                    }


                    break;
                }

            case "spawn":
                {
                    var data = JsonUtility.FromJson<SpawnJsonData>(message);
                    Transform tr = transform.Find(data.name);

                    if (tr != null)
                    {
                        tr.position = mapRenderer.GetWorldPosition(data.x, data.y);
                        break;
                    }

                    GameObject playerObject = Instantiate(characterPrefab, mapRenderer.GetWorldPosition(data.x, data.y), Quaternion.identity, transform);
                    playerObject.name = data.name;

                    UseMeshyMesh script = playerObject.GetComponent<UseMeshyMesh>();
                    script.SetMesh(data.meshyId);

                    cameraManager.Follow(playerObject);
                    await Task.Delay(500);
                    cameraManager.SetZoomLevel(1f);
                    break;
                }

            case "move":
                {
                    var data = JsonUtility.FromJson<MoveJsonData>(message);
                    GameObject character = transform.Find(data.name).gameObject;


                    cameraManager.Follow(character);
                    await Task.Delay(500);
                    cameraManager.SetZoomLevel(1.5f);
                    await Task.Delay(500);

                    for (int i = 0; i < data.positions.Count; i++)
                    {
                        var tcs = new TaskCompletionSource<object>();
                        LeanTween.move(character, mapRenderer.GetWorldPosition((int)data.positions[i].x, (int)data.positions[i].y), 0.8f)
                            .setEaseOutExpo()
                            .setOnComplete(tcs.SetResult);
                        await tcs.Task;
                    }
                    break;
                }

            case "zoom":
                {
                    var data = JsonUtility.FromJson<ZoomJsonData>(message);
                    GameObject character = transform.Find(data.name).gameObject;


                    await Task.Delay(1000);
                    cameraManager.SetZoomLevel(1.5f);
                    await Task.Delay(500);
                    cameraManager.Follow(character);
                    await Task.Delay(500);
                    cameraManager.SetZoomLevel(1f);
                    break;
                }

            case "roll":
                {
                    var data = JsonUtility.FromJson<RollJsonData>(message);
                    var total = await diceSpawner.RollDice(data.values, cameraManager);
                    SendString("{\"type\": \"roll\", \"value\": " + total + "}");
                    break;
                }

            case "talk":
                {
                    var data = JsonUtility.FromJson<TalkJsonData>(message);
                    textToSpeech.TalkGlobal(data.message);
                    break;
                }

            case "music":
                {
                    var data = JsonUtility.FromJson<MusicJsonData>(message);
                    musicPlayer.PlayMusic(data.category);
                    break;
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

    [Serializable]
    private class SpawnJsonData : JsonData
    {
        public string name;
        public int x;
        public int y;
        public string meshyId;
    }

    [Serializable]
    private class MoveJsonData : JsonData
    {
        public string name;
        public List<Coordinate> positions;
    }

    [Serializable]
    private class ZoomJsonData : JsonData
    {
        public string name;
    }

    [Serializable]
    private class Coordinate
    {
        public int x;
        public int y;
    }

    [Serializable]
    private class RollJsonData : JsonData
    {
        public int[] values;
    }

    [Serializable]
    private class MapJsonData : JsonData
    {
        public string map;

        public Entity[] entities;
    }

    [Serializable]
    private class Entity : JsonData
    {
        public string name;

        public string meshyId;

        public int x;
        public int y;

    }


    [Serializable]
    private class MusicJsonData : JsonData
    {
        public string category;
    }

    [Serializable]
    private class TalkJsonData : JsonData
    {
        public string name;
        public string message;
    }
}
