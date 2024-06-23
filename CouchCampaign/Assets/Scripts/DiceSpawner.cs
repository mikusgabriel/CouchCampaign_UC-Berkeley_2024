using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using UnityEngine;

public class DiceSpawner : MonoBehaviour
{
    [SerializeField]
    private GameObject map;

    [Header("Dice prefabs")]
    [SerializeField]
    private GameObject d4;
    [SerializeField]
    private GameObject d6;
    [SerializeField]
    private GameObject d8;
    [SerializeField]
    private GameObject d10;
    [SerializeField]
    private GameObject d12;
    [SerializeField]
    private GameObject d20;


    public async Task<int> RollDice(int[] diceArray)
    {
        var diceRollScripts = new List<DiceRoll>(diceArray.Length);
        var mapWidth = map.GetComponent<Terrain>().terrainData.size.x;
        var mapLength = map.GetComponent<Terrain>().terrainData.size.z;

        foreach (var diceValue in diceArray)
        {
            var dicePosX = Random.Range(mapWidth / 4, mapWidth / 2);
            var dicePosY = Random.Range(0.5f, 0.75f);
            var dicePosZ = Random.Range(mapLength / 8, mapLength / 6);

            var diceRotation = Random.Range(0f, 90f);

            // YOU CAN CHANGE INITIAL POSITION HERE
            GameObject dice = Instantiate(GetPrefabFromDiceValue(diceValue), new Vector3(map.transform.position.x + dicePosX, map.transform.position.y + dicePosY, map.transform.position.z + dicePosZ), new Quaternion(0, 0, diceRotation, 0));
            dice.transform.localScale /= 6;

            dice.GetComponent<Rigidbody>().AddTorque(new Vector3(3f, 1f, 1f), ForceMode.Impulse);
            dice.GetComponent<Rigidbody>().AddForce(new Vector3(0, -1f, 5f), ForceMode.Impulse);

            diceRollScripts.Add(dice.GetComponent<DiceRoll>());
        }

        int diceMoving = diceArray.Length;
        var diceTotalResult = 0;
        while (diceMoving > 0)
        {
            await Task.Delay(500);
            foreach (DiceRoll script in diceRollScripts)
            {
                if (script.gameObject.GetComponent<Rigidbody>().velocity != Vector3.zero)
                {
                    break;
                }
                else
                {
                    diceTotalResult += script.GetCurrentDiceValue();
                    diceMoving--;
                }
            }

        }

        return diceTotalResult;
    }

    private GameObject GetPrefabFromDiceValue(int dice)
    {
        switch (dice)
        {
            case 4:
                return d4;

            case 6:
                return d6;

            case 8:
                return d8;

            case 10:
                return d10;

            case 12:
                return d12;

            case 20:
                return d20;

            default:
                Debug.Log("Unvalid Dice Type");
                return d6;
        }
    }
}
