import { type ReactNode, createContext, useContext, useEffect, useState } from "react";
import useServer from "./ServerContext";

export type Status = "create" | "wait" | "play";
const statusContext = createContext<Status | null>(null);

type StatusProviderProps = { children: ReactNode };
export function StatusProvider({ children }: StatusProviderProps) {
    const server = useServer();
    const [status, setStatus] = useState<Status>("wait");

    useEffect(
        () =>
            server.addOnMessage((message) => {
                if (message.type === "status") {
                    setStatus(message.status);
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
