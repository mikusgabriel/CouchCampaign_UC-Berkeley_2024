using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MusicPlayer : MonoBehaviour
{
    // Start is called before the first frame update

    public AudioSource audiosource;
    public void PlayMusic(string category)
    {
        
        audiosource.Stop();
        var audioClip = Resources.Load<AudioClip>($"Music/{category}/{Random.Range(1,5)}");
        audiosource.clip = audioClip;
        audiosource.Play();
    }

    
}