import type { Status } from "./StatusContext";
import type { User } from "./UserContext";

export default class Server {
    constructor() {
        this.connect();
    }

    public async connect() {
        this.websocket = new WebSocket("/api/player/ws");

        this.websocket.addEventListener("open", () => this.onConnected?.(true));
        this.websocket.addEventListener("close", () => this.onConnected?.(false));
        this.websocket.addEventListener("error", () => this.onConnected?.(false));

        return new Promise<Event>((res, rej) => {
            this.websocket.addEventListener("open", res);
            this.websocket.addEventListener("close", rej);
            this.websocket.addEventListener("error", rej);
        });
    }

    public disconnect() {
        this.websocket.close();
    }

    public get connected(): boolean {
        return this.websocket.readyState === this.websocket.OPEN;
    }

    public onConnected: ((connected: boolean) => void) | undefined;

    public addOnMessage(handler: ServerMessageHandler) {
        const f = (e: MessageEvent) => {
            handler(JSON.parse(e.data), () => this.websocket.removeEventListener("message", f));
        };

        this.websocket.addEventListener("message", f);
        return () => this.websocket.removeEventListener("message", f);
    }

    public send(message: ClientMessage) {
        this.websocket.send(JSON.stringify(message));
    }

    private websocket!: WebSocket;
}

type StatusServerMessage = { type: "status"; status: Status["status"]; data: Record<string, unknown> | undefined };
type UserServerMessage = { type: "user"; user: User };
type ServerMessage = StatusServerMessage | UserServerMessage;
type ServerMessageHandler = (message: ServerMessage, remove: () => void) => void;

type EndTurnClientMessage = { type: "end-turn" };
type VoiceClientMessage = { type: "voice"; recording: string };
type ClientMessage = EndTurnClientMessage | VoiceClientMessage;
