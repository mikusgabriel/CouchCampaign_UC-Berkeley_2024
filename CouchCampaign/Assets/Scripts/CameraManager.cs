using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraManager : MonoBehaviour
{
    [Header("Camera")]
    [SerializeField]
    private Camera cam;

    private float zoomLevel = 9;

    private int tweenIdZoomLevel;
    private int tweenIdFollowX;
    private int tweenIdFollowZ;

    public void SetZoomLevel(float level)
    {
        LeanTween.cancel(tweenIdZoomLevel);
        var angle = cam.transform.rotation.eulerAngles.x;

        var y = Mathf.Sin(Mathf.Deg2Rad * angle) * level;
        var z = Mathf.Cos(Mathf.Deg2Rad * angle) * level;
        var pos = new Vector3(0, y, z);
        var distance = (cam.transform.position - pos).magnitude;

        tweenIdZoomLevel = LeanTween.moveLocal(cam.gameObject, pos, 0.1f * distance).setEaseOutExpo().setOnComplete(() => zoomLevel = level).id;
    }

    public void Follow(GameObject obj)
    {
        StopFollow();
        tweenIdFollowX = LeanTween.followDamp(transform, obj.transform, LeanProp.x, 0.5f).setEaseOutExpo().id;
        tweenIdFollowZ = LeanTween.followDamp(transform, obj.transform, LeanProp.z, 0.5f).setEaseOutExpo().id;
    }

    public void StopFollow()
    {
        LeanTween.cancel(tweenIdFollowX);
        LeanTween.cancel(tweenIdFollowZ);
    }
}
