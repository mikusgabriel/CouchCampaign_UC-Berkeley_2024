import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { FadeDiv } from "@/components/ui/FadeDiv";
import useStatus from "@/lib/StatusContext";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { AnimatePresence } from "framer-motion";
import { Check, LoaderCircle } from "lucide-react";
import { useState } from "react";

export default function ChoicePage() {
    const status = useStatus();
    if (status.status !== "choice") return "no";
    const [selected, setSelected] = useState<Record<string, string[]>>({});
    const [tab, setTab] = useState(0);

    const { mutate, isPending, error } = useMutation({
        mutationFn: async () => {
            return await axios.post("/api/player/choice", { selected });
        },
    });

    return (
        <div className="p-4 gap-4 flex flex-col flex-1">
            <h2 className="text-center text-xl text-foreground/80">Couch Campaign</h2>
            <h1 className="text-center text-3xl font-semibold">Character creation</h1>

            <div className="divide-y flex-1">
                {status.choices.map(({ name, "choice-count": count, options }, i) => (
                    <div className="flex flex-col p-4 overflow-y-hidden" key={name}>
                        <div className="flex justify-between items-center gap-4 mb-2">
                            <h1 className="text-xl">{name}</h1>
                            {tab !== i ? (
                                <Button onClick={() => setTab(i)} variant="ghost" size="sm">
                                    Change
                                </Button>
                            ) : (
                                <span>Choose {count}</span>
                            )}
                        </div>

                        <AnimatePresence>
                            {tab === i ? (
                                <Card className="overflow-y-scroll divide-y py-2">
                                    {options.map((o) => (
                                        <FadeDiv className="grid" key={o.name}>
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                className="flex justify-between gap-4 items-center border-none rounded-none"
                                                onClick={() => {
                                                    setSelected((s) => {
                                                        if (!(name in s)) {
                                                            return { ...selected, [name]: [o.name] };
                                                        }
                                                        if (s[name].includes(o.name)) {
                                                            return {
                                                                ...s,
                                                                [name]: s[name].filter((n) => n !== o.name),
                                                            };
                                                        }
                                                        if (s[name].length >= count) {
                                                            return { ...s, [name]: [...s[name].slice(1), o.name] };
                                                        }
                                                        return { ...s, [name]: [...s[name], o.name] };
                                                    });
                                                }}
                                            >
                                                <h1>{o.name}</h1>

                                                <span className="w-4 text-xs flex">
                                                    {selected[name]?.includes(o.name) && <Check />}
                                                </span>
                                            </Button>
                                        </FadeDiv>
                                    ))}
                                </Card>
                            ) : (
                                <FadeDiv>{selected[name]?.join(" · ")}</FadeDiv>
                            )}
                        </AnimatePresence>
                    </div>
                ))}
            </div>

            <div className="h-fit grid">
                {error && <p className="text-destructive">An error occured, please try again</p>}

                <Button
                    className="m-2"
                    size="lg"
                    onClick={() => mutate()}
                    disabled={isPending || status.choices.some((c) => c["choice-count"] !== selected[c.name]?.length)}
                >
                    {isPending && <LoaderCircle className="animate-spin" />}
                    Create character
                </Button>
            </div>
        </div>
    );
}
