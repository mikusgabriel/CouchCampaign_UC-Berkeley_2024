using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using GLTFast;
using System.Threading.Tasks;
using System.IO;
using CandyCoded.env;


public class UseMeshyMesh : MonoBehaviour
{
    public GltfImport gltf;


    private readonly string meshyApiKey = env.variables["MeshyKey"];

    

    public async void SetMesh(string meshId)
    {
        if (await LoadModel(meshId)) return;
       
        StartCoroutine(MakeRequest(meshyApiKey, meshId));
    }


    IEnumerator MakeRequest(string apiKey, string meshId)
    {
        Debug.Log("Beofre get url");
        string url = "https://api.meshy.ai/v2/text-to-3d/" + meshId;
        var glbUrl = "";

        using UnityWebRequest webRequest = UnityWebRequest.Get(url);
        webRequest.SetRequestHeader("Authorization", $"Bearer {apiKey}");

        yield return webRequest.SendWebRequest();


        if (webRequest.result == UnityWebRequest.Result.ConnectionError ||
            webRequest.result == UnityWebRequest.Result.ProtocolError)
        {
            Debug.LogError($"Meshy download error: {webRequest.error}");
            yield break;
        }

        // Timer can change based on Meshy Subscription
        yield return new WaitForSeconds(5f);

        try
        {
            var jsonResponse = webRequest.downloadHandler.text;
            ApiResponseData responseData = JsonUtility.FromJson<ApiResponseData>(jsonResponse);

            if (responseData.status != "SUCCEEDED")
            {

                SetMesh(meshId);
                yield break;
            }

            glbUrl = responseData.model_urls.glb;
        }
        catch (Exception ex)
        {
            Debug.LogError($"Error parsing Meshy JSON: {ex.Message}");
        }


        using UnityWebRequest modelReq = UnityWebRequest.Get(glbUrl);
        yield return modelReq.SendWebRequest();

        if (modelReq.result == UnityWebRequest.Result.ConnectionError ||
                modelReq.result == UnityWebRequest.Result.ProtocolError)
        {
            Debug.LogError($"Meshy GLB download error: {modelReq.error}");
            yield break;
        }

        SaveModel(meshId, modelReq.downloadHandler.data);
        _ = AddModel(modelReq.downloadHandler.data);
    }


    async void SaveModel(string meshId, byte[] data)
    {
        Directory.CreateDirectory(".cache");
        var file = File.Create($".cache/{meshId}.glb");
        await file.WriteAsync(data);
    }


    async Task<bool> LoadModel(string meshId)
    {
        if (!File.Exists($".cache/{meshId}.glb")) return false;
        if (!await gltf.LoadFile($".cache/{meshId}.glb")) return false;
        if (!await gltf.InstantiateMainSceneAsync(transform)) return false;

        var mesh = transform.Find("Mesh1");
        var renderer = mesh.GetComponent<MeshRenderer>();
        mesh.localPosition = new Vector3(mesh.localPosition.x, renderer.localBounds.size.y / 2 + 0.15f, mesh.localPosition.z);
        return true;
    }


    async Task<bool> AddModel(byte[] data)
    {
        if (!await gltf.LoadGltfBinary(data)) return false;
        if (!await gltf.InstantiateMainSceneAsync(transform)) return false;

        var mesh = transform.Find("Mesh1");
        var renderer = mesh.GetComponent<MeshRenderer>();
        mesh.localPosition = new Vector3(mesh.localPosition.x, renderer.localBounds.size.y / 2 + 0.15f, mesh.localPosition.z);
        return true;
    }


    void Awake()
    {
        gltf = new GltfImport();
    }


    // JSON response
    [Serializable]
    private class ApiResponseData
    {
        public ModelUrlData model_urls;

        public string status;
    }


    [Serializable]
    private class ModelUrlData
    {
        public string glb;
    }
}
