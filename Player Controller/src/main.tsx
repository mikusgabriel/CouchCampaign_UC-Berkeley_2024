import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import { AuthProvider } from "./lib/AuthContext.tsx";
import { ServerProvider } from "./lib/ServerContext.tsx";
import { StatusProvider } from "./lib/StatusContext.tsx";

import "./index.css";

const queryClient = new QueryClient();

// biome-ignore lint/style/noNonNullAssertion: Yeah no shit
ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <QueryClientProvider client={queryClient}>
            <AuthProvider>
                <ServerProvider>
                    <StatusProvider>
                        <App />
                    </StatusProvider>
                </ServerProvider>
            </AuthProvider>
        </QueryClientProvider>
    </React.StrictMode>,
);
