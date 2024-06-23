using OpenAI;
using OpenAI.Audio;
using UnityEngine;
using CandyCoded.env;

public class TextToSpeech : MonoBehaviour
{
    [SerializeField]
    private AudioSource globalAudioSource;

    private OpenAIClient api;


    void Awake()
    {
        api = new OpenAIClient(env.variables["OpenaiKey"]);
    }


    public async void Talk(string sentence, AudioSource source)
    {
        var request = new SpeechRequest(sentence);
        var result = await api.AudioEndpoint.CreateSpeechAsync(request);

        globalAudioSource.PlayOneShot(result.Item2);
    }


    public void TalkGlobal(string sentence)
    {
        globalAudioSource.Pause();
        Talk(sentence, globalAudioSource);
    }
}
