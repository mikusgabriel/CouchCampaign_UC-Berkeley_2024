import { Button } from "@/components/ui/Button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import useAuth from "@/lib/AuthContext";
import useStatus from "@/lib/StatusContext";
import useUser from "@/lib/UserContext";
import { cn } from "@/lib/utils";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { LoaderCircle, Smile, Sword, User } from "lucide-react";

export default function HomePage() {
    const { loading, logout } = useAuth();
    const status = useStatus();
    const user = useUser();

    const getAt = (x: number, y: number) => {
        if (status.status !== "play") return undefined;
        const move = status.options.move.find((m) => m.x === x && m.y === y);
        if (move) return { action: "move", ...move };
        const fight = status.options.fight.find((f) => f.x === x && f.y === y);
        if (fight) return { action: "fight", ...fight };
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
                    <TabsContent value="play">
                        {status.status === "play" && (
                            <div className="flex flex-col">
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
                                                        !getAt(x, y)
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
                                                    {status.options.allies.find((f) => f.x === x && f.y === y) && (
                                                        <Smile />
                                                    )}
                                                    {status.options.fight.find((f) => f.x === x && f.y === y) && (
                                                        <Sword />
                                                    )}
                                                </Button>
                                            ))}
                                        </div>
                                    ))}
                                </div>

                                {error && (
                                    <p className="text-destructive">An error occured while sending your choice</p>
                                )}
                            </div>
                        )}
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
