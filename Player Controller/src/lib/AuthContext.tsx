import LoginPage from "@/pages/Login";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { type ReactNode, createContext, useContext, useEffect, useState } from "react";

type Auth = {
    loggedIn: boolean;
    loading: boolean;
    login: (name: string) => void;
    logout: () => void;
};
const authContext = createContext<Auth | null>(null);

type ProviderProps = { children: ReactNode };
export function AuthProvider({ children }: ProviderProps) {
    const [userId, setUserId] = useState<string | null>(localStorage.getItem("name"));

    useEffect(() => {
        if (userId) localStorage.setItem("name", userId);
        else localStorage.removeItem("name");
    }, [userId]);

    const loginAction = useMutation({
        mutationFn: async (name: string) => {
            if (userId) return;
            return await axios.post("/api/login", { name });
        },
        onSuccess(data) {
            if (data) setUserId(data.data.id);
        },
    });

    const logoutAction = useMutation({
        mutationFn: async () => {
            if (!userId) return;
            return await axios.post("/api/logout", {});
        },
        onSuccess() {
            setUserId(null);
        },
    });

    const Provider = authContext.Provider;
    return (
        <Provider
            value={{
                loggedIn: !!userId,
                loading: loginAction.isPending || logoutAction.isPending,
                login: loginAction.mutate,
                logout: logoutAction.mutate,
            }}
        >
            {userId ? children : <LoginPage />}
        </Provider>
    );
}

export default function useAuth() {
    const auth = useContext(authContext);
    if (!auth) throw "Auth not loaded";
    return auth;
}
