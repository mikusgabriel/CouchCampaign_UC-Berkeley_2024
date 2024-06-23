import type { ClasseKey } from "@/lib/data/classes";
import type { RaceKey } from "@/lib/data/races";
import LoadingPage from "@/pages/Loading";
import { type ReactNode, createContext, useContext, useEffect, useState } from "react";
import useServer from "./ServerContext";
import useStatus from "./StatusContext";

export type User = { name: string; race: RaceKey; classe: ClasseKey; meshyId: string; x: number; y: number };
const userContext = createContext<User | null>(null);

type ProviderProps = { children: ReactNode };
export function UserProvider({ children }: ProviderProps) {
    const server = useServer();
    const { status } = useStatus();
    const [user, setUser] = useState<User | null>(getStoredUser());

    useEffect(
        () =>
            server.addOnMessage((message) => {
                if (message.type === "user") {
                    setUser(message.user);
                }
            }),
        [server.addOnMessage],
    );

    useEffect(() => {
        if (user) localStorage.setItem("user", JSON.stringify(user));
        else localStorage.removeItem("user");
    }, [user]);

    if (!user && status !== "create") {
        return <LoadingPage />;
    }

    const Provider = userContext.Provider;
    return <Provider value={user}>{children}</Provider>;
}

export default function useUser() {
    const user = useContext(userContext);
    if (!user) throw "User not loaded";
    return user;
}

function getStoredUser() {
    const ls = localStorage.getItem("user");

    if (ls) return JSON.parse(ls) as User;
    return null;
}
