using System.Collections.Generic;
using UnityEngine;

public class DiceRoll : MonoBehaviour
{
    [SerializeField]
    private Transform dice;

    public int GetCurrentDiceValue()
    {
        Vector3 downV = Vector3.up;
        Transform downF = null;

        foreach (Transform face in dice)
        {
            if (face.name.StartsWith("_")) continue;

            List<Vector3> normals = new();
            Mesh mesh = face.GetComponent<MeshFilter>().mesh;
            mesh.GetNormals(normals);

            if ((dice.rotation * normals[0]).y < downV.y)
            {
                downV = (dice.rotation * normals[0]);
                downF = face;
            }
        }

        return int.Parse(downF.name);
    }
}
