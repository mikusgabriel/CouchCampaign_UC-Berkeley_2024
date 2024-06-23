import VoiceRecorder from "@/components/VoiceRecorder";
import { Button } from "@/components/ui/Button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import useAuth from "@/lib/AuthContext";
import useServer from "@/lib/ServerContext";
import useStatus, { type StatusPlay } from "@/lib/StatusContext";
import useUser from "@/lib/UserContext";
import { cn } from "@/lib/utils";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { LoaderCircle, MessageCircle, Smile, Sword, User } from "lucide-react";
import { useEffect, useState } from "react";

export default function HomePage() {
    const { loading, logout } = useAuth();
    const server = useServer();
    const status = useStatus();
    const user = useUser();
    const [playData, setPlayData] = useState<StatusPlay["options"]>({
        move: [],
        abilities: [],
        allies: [],
        fight: [],
        talk: [],
    });

    useEffect(() => {
        if (status.status === "play") {
            setPlayData(status.options);
        }
    }, [status]);

    const getAt = (x: number, y: number) => {
        const fight = playData.fight.find((f) => f.x === x && f.y === y);
        if (fight) return { action: "fight", ...fight };
        const allies = playData.allies.find((f) => f.x === x && f.y === y);
        if (allies) return undefined;
        const talk = playData.talk.find((f) => f.x === x && f.y === y);
        if (talk) return { action: "talk", ...talk };
        const move = playData.move.find((m) => m[0] === x && m[1] === y);
        if (move) return { action: "move", x: move[0], y: move[1] };
    };

    const { mutate, isPending, error } = useMutation({
        mutationFn: async ({ x, y }: { x: number; y: number }) => {
            const action = getAt(x, y);
            if (!action) return;
            return await axios.post("/api/player/play", action);
        },
    });

    return (
        <>
            <div className="flex items-center justify-between px-2 pt-2">
                <h1 className="font-semibold text-2xl">Couch Campaign</h1>

                <div className="flex items-center gap-2">
                    <p>{user.name}</p>
                    <Button variant="ghost" size="sm" onClick={() => logout()}>
                        {loading && <LoaderCircle className="animate-spin" />}
                        Log out
                    </Button>
                </div>
            </div>

            <main className="flex-1 p-4">
                <Tabs defaultValue="spells">
                    <TabsList className="w-full justify-around">
                        <TabsTrigger value="spells">Spells</TabsTrigger>
                        <TabsTrigger value="inventory">Inventory</TabsTrigger>
                        <TabsTrigger value="play" disabled={status.status !== "play"}>
                            Turn
                        </TabsTrigger>
                    </TabsList>

                    <TabsContent value="spells">Make changes to your account here.</TabsContent>
                    <TabsContent value="inventory">Change your password here.</TabsContent>
                    <TabsContent value="play" className="flex flex-col">
                        {status.status === "talk" && (
                            <div className="flex flex-col gap-2 px-8 py-4">
                                <VoiceRecorder />

                                <Button onClick={() => server.send({ type: "end-turn" })}>End conversation</Button>
                            </div>
                        )}

                        <div className="flex mx-auto">
                            {gen(user.x).map((x) => (
                                <div className="flex flex-col-reverse" key={`user-x-${x}`}>
                                    {gen(user.y).map((y) => (
                                        <Button
                                            disabled={
                                                isPending ||
                                                x < 0 ||
                                                x >= 80 ||
                                                y < 0 ||
                                                y >= 80 ||
                                                !getAt(x, y) ||
                                                status.status !== "play"
                                            }
                                            className={cn(
                                                (x < 0 || x >= 80 || y < 0 || y >= 80) && "grayscale",
                                                user.x === x && user.y === y && "!opacity-100",
                                            )}
                                            variant="ghost"
                                            size="icon"
                                            key={`user-y-${y}`}
                                            onClick={() => mutate({ x, y })}
                                        >
                                            {user.x === x && user.y === y && <User />}
                                            {playData.allies.find((a) => a.x === x && a.y === y) && <Smile />}
                                            {playData.fight.find((f) => f.x === x && f.y === y) && <Sword />}
                                            {playData.talk.find((t) => t.x === x && t.y === y) && <MessageCircle />}
                                        </Button>
                                    ))}
                                </div>
                            ))}
                        </div>

                        {error && <p className="text-destructive">An error occured while sending your choice</p>}

                        <div className="flex flex-col gap-1 pt-4">
                            {playData.abilities.map((a) => (
                                <div key={a.name}>
                                    <span>{a.name}</span> · <span className="text-sm">{a.description}</span>
                                </div>
                            ))}
                        </div>
                    </TabsContent>
                </Tabs>
            </main>
        </>
    );
}

function gen(pivot: number) {
    const n = Math.max(3, Math.min(pivot, 76));
    return [n + 5, n + 4, n + 3, n + 2, n + 1, n, n - 1, n - 2, n - 3, n - 4, n - 5];
}
