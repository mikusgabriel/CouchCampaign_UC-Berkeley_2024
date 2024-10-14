using System.Collections.Generic;
using UnityEngine;

public class MapRenderer : MonoBehaviour
{
    readonly Dictionary<string, float> TILE_COLORS = new Dictionary<string, float>
    {
        { ColorUtility.ToHtmlStringRGB(new Color(0f, 0.5f, 0f)), 0.10f },               // grass
        { ColorUtility.ToHtmlStringRGB(new Color(0.647f, 0.165f, 0.165f)) , 0.08f },    // path-level0
        { ColorUtility.ToHtmlStringRGB(new Color(0.823f, 0.705f, 0.549f)) , 0.30f },    // path_level1
        { ColorUtility.ToHtmlStringRGB(new Color(0.627f, 0.321f, 0.176f)) , 0.63f },    // path_level2
        { ColorUtility.ToHtmlStringRGB(new Color (0.545f, 0.271f, 0.075f)), 0.96f },    // path_level3
        { ColorUtility.ToHtmlStringRGB(new Color(0f, 0f, 1f)), 0.0f },                  // water
        { ColorUtility.ToHtmlStringRGB(new Color(0f, 0.392f, 0f)) , 0.10f },            // forest
        { ColorUtility.ToHtmlStringRGB(new Color(1f, 1f, 0f)) ,0.05f },                 // sand
        { ColorUtility.ToHtmlStringRGB(new Color(1f, 0.549f, 0f)) , 0.12f },            // bridge
        { ColorUtility.ToHtmlStringRGB(new Color(0.502f, 0.502f, 0.502f)) , 0.33f },    // rocklevel1
        { ColorUtility.ToHtmlStringRGB(new Color(0.663f, 0.663f, 0.663f)) , 0.66f },    // rocklevel2
        { ColorUtility.ToHtmlStringRGB(new Color(0.827f, 0.827f, 0.827f)), 0.99f }  // rocklevel3
    };



    [SerializeField]
    private Terrain terrain;
    [SerializeField]
    private Material material;


    private Texture2D texture;

    private float[,] heights;


    public void LoadMapFromFile(byte[] imgBytes)
    {
        texture = new Texture2D(2, 2);
        texture.LoadImage(imgBytes); // LoadImage auto-resizes texture dimensions
        material.mainTexture = texture;
    }


    public Vector3 GetWorldPosition(int x, int y)
    {
        float scaleX = terrain.terrainData.size.x / 80;
        float scaleZ = terrain.terrainData.size.z / 40;
        float yHeight = 0f;

        Color color = texture.GetPixel(x, y);
        string colorString = ColorUtility.ToHtmlStringRGB(color);
        if (TILE_COLORS.TryGetValue(colorString, out float height))
        {
            yHeight = height;
        }

        return new Vector3(x * scaleX + 0.075f, yHeight, y * scaleZ + 0.075f);
    }



    public void SetTerrainHeight()
    {
        int xRes = terrain.terrainData.heightmapResolution;
        int yRes = terrain.terrainData.heightmapResolution;

        heights = new float[xRes, yRes];

        for (int y = 0; y < yRes; y++)
        {
            for (int x = 0; x < xRes; x++)
            {
                int texX = Mathf.FloorToInt((float)x / xRes * texture.width);
                int texY = Mathf.FloorToInt((float)y / yRes * texture.height);
                Color color = texture.GetPixel(texX, texY);

                string colorString = ColorUtility.ToHtmlStringRGB(color);
                if (TILE_COLORS.TryGetValue(colorString, out float height))
                {
                    heights[y, x] = height;
                }
                else
                {
                    heights[y, x] = 0f; // default height if color not found
                }
            }
        }

        terrain.terrainData.SetHeights(0, 0, heights);
    }
}
