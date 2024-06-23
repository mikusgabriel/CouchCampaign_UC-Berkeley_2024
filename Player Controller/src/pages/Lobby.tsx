import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import useStatus from "@/lib/StatusContext";
import useUser from "@/lib/UserContext";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { LoaderCircle, UserRoundX } from "lucide-react";

export default function LobbyPage() {
    const status = useStatus();
    const user = useUser();

    const { mutate, isPending, error } = useMutation({
        mutationFn: async () => {
            return await axios.post("/api/player/start");
        },
    });

    const deletePlayer = useMutation({
        mutationFn: async (name: string) => {
            return await axios.post("/api/player/kick", { name });
        },
    });

    if (status.status !== "lobby") return "no";
    const { players } = status;

    return (
        <div className="p-8 gap-4 flex flex-col">
            <h2 className="text-center text-xl text-foreground/80">Couch Campaign</h2>
            <h1 className="text-center text-3xl font-semibold">Lobby</h1>

            <Card className="gap-2 divide-y pt-2">
                {players.map((p) => (
                    <div className="flex justify-between gap-4 items-center px-2 pb-2" key={p.name}>
                        <div>
                            <h1 className="font-semibold">{p.name}</h1>
                            <p>
                                {p.race} · {p.classe}
                            </p>
                        </div>

                        {p.name === user.name ? (
                            <span className="text-foreground/80">you</span>
                        ) : (
                            <Button variant="ghost" size="icon" onClick={() => deletePlayer.mutate(p.name)}>
                                <UserRoundX />
                            </Button>
                        )}
                    </div>
                ))}
            </Card>

            <div className="h-fit grid">
                {error && <p className="text-destructive">An error occured, please try again</p>}

                <Button className="m-2" size="lg" onClick={() => mutate()} disabled={isPending || players.length < 2}>
                    {isPending && <LoaderCircle className="animate-spin" />}
                    Start game
                </Button>
            </div>
        </div>
    );
}
