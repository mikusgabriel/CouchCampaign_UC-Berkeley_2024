import LoadingPage from "@/pages/Loading";
import { type ReactNode, createContext, useContext, useEffect, useMemo, useState } from "react";
import useAuth from "./AuthContext";
import Server from "./server";

const serverContext = createContext<Server | null>(null);

type ProviderProps = { children: ReactNode };
export function ServerProvider({ children }: ProviderProps) {
    const { loggedIn } = useAuth();
    const server = useMemo(() => new Server(), []);
    const [connected, setConnected] = useState(server.connected);

    useEffect(() => {
        server.onConnected = setConnected;

        return () => {
            server.onConnected = undefined;
        };
    }, [server]);

    useEffect(() => {
        if (loggedIn) server.connect();
        else server.disconnect();
    }, [loggedIn, server.connect, server.disconnect]);

    if (!connected) {
        return <LoadingPage />;
    }

    const Provider = serverContext.Provider;
    return <Provider value={server}>{children}</Provider>;
}

export default function useServer() {
    const server = useContext(serverContext);
    if (!server) throw "Server not loaded";
    return server;
}
