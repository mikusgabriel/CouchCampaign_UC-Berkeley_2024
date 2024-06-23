import { Button } from "@/components/ui/Button";
import useStatus from "@/lib/StatusContext";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { Check, LoaderCircle } from "lucide-react";
import { useState } from "react";

export default function ChoicePage() {
    const status = useStatus();
    const [selected, setSelected] = useState<string[]>([]);

    const { mutate, isPending, error } = useMutation({
        mutationFn: async () => {
            if (selected.length !== count) return;
            return await axios.post("/api/player/choice", { selected });
        },
    });

    if (status.status !== "choice") return "no";
    const { name, description, options, count } = status;

    return (
        <div className="p-4 gap-4 flex flex-col">
            <h2 className="text-center text-xl text-foreground/80">Couch Campaign</h2>
            <h1 className="text-center text-3xl font-semibold">{name}</h1>
            <h3 className="text-xl pb-2">{description}</h3>

            <div className="flex flex-col justify-stretch gap-1">
                {options.map((o) => (
                    <Button
                        variant="ghost"
                        size="sm"
                        className="flex justify-between gap-4 items-center"
                        onClick={() => {
                            setSelected((s) => {
                                if (s.includes(o.name)) return s.filter((n) => n !== o.name);
                                if (s.length >= count) return [...s.slice(1), o.name];
                                return [...s, o.name];
                            });
                        }}
                        key={o.name}
                        type="button"
                    >
                        <h1>{o.name}</h1>

                        <span className="w-4 text-xs flex">{selected.includes(o.name) && <Check />}</span>
                    </Button>
                ))}
            </div>

            <div className="h-fit grid">
                {error && <p className="text-destructive">An error occured, please try again</p>}

                <Button
                    className="m-2"
                    size="lg"
                    onClick={() => mutate()}
                    disabled={isPending || selected.length !== count}
                >
                    {isPending && <LoaderCircle className="animate-spin" />}
                    Create character
                </Button>
            </div>
        </div>
    );
}
