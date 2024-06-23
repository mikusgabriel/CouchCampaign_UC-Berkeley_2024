import { type ReactNode, createContext, useContext, useEffect, useState } from "react";
import useServer from "./ServerContext";

const statusContext = createContext<Status | null>(null);

type StatusProviderProps = { children: ReactNode };
export function StatusProvider({ children }: StatusProviderProps) {
    const server = useServer();
    const [status, setStatus] = useState<Status>({ status: "wait" });

    useEffect(
        () =>
            server.addOnMessage((message) => {
                console.log("🚀 ~ server.addOnMessage ~ message:", message);
                if (message.type === "status") {
                    setStatus({ status: message.status, ...message.data } as Status);
                }
            }),
        [server.addOnMessage],
    );

    const Provider = statusContext.Provider;
    return <Provider value={status}>{children}</Provider>;
}

export default function useStatus() {
    const status = useContext(statusContext);
    if (!status) throw "Status not loaded";
    return status;
}

type StatusCreate = { status: "create" };
type StatusChoice = {
    status: "choice";
    name: "string";
    description: string;
    options: { name: string }[];
    count: number;
};
type StatusLobby = { status: "lobby"; players: { name: string; race: string; classe: string }[] };
type StatusWait = { status: "wait" };
export type StatusPlay = {
    status: "play";
    options: {
        move: [number, number][];
        talk: { x: number; y: number; name: string }[];
        fight: { x: number; y: number; name: string }[];
        allies: { x: number; y: number; name: string }[];
        abilities: { name: string; description: string }[];
    };
};
type StatusSpeak = { status: "talk"; to: string };
export type Status = StatusCreate | StatusChoice | StatusLobby | StatusWait | StatusPlay | StatusSpeak;
