import useServer from "@/lib/ServerContext";
import { Mic } from "lucide-react";
import { useEffect } from "react";
import { useAudioRecorder } from "react-audio-voice-recorder";
import { Button } from "./ui/Button";

export default function VoiceRecorder() {
    const server = useServer();

    const { startRecording, stopRecording, recordingBlob, isRecording, recordingTime } = useAudioRecorder();

    useEffect(() => {
        if (!recordingBlob) return;

        const sendRecording = async () => {
            server.send({
                type: "voice",
                recording: await blobToDataUrl(recordingBlob),
            });
        };

        sendRecording();
    }, [recordingBlob, server]);

    return (
        <Button
            className="rounded-full gap-2 m-2 p-6"
            onClick={() => {
                isRecording ? stopRecording() : startRecording();
            }}
        >
            <h1 className="h1">{isRecording ? "Stop" : <Mic />}</h1>
            <h1 className="h1">{recordingTime}</h1>
        </Button>
    );
}

const blobToDataUrl = (blob: Blob) => {
    return new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            resolve(reader.result as string);
        };
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
};
