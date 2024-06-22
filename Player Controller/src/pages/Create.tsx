import useAuth from "@/lib/AuthContext";
import type { ClasseKey } from "@/lib/data/classes";
import classes from "@/lib/data/classes";
import type { RaceKey } from "@/lib/data/races";
import races from "@/lib/data/races";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { AnimatePresence } from "framer-motion";
import { LoaderCircle } from "lucide-react";
import { useState } from "react";

import { ClasseCard, RaceCard } from "@/components/ChoiceCards";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { FadeDiv } from "@/components/ui/FadeDiv";
import { Label } from "@/components/ui/Label";
import { Separator } from "@/components/ui/Separator";
import { Textarea } from "@/components/ui/TextArea";

export default function CreatePage() {
    const { logout, userId } = useAuth();
    const [tab, setTab] = useState<"race" | "classe" | "desc">("race");
    const [race, setRace] = useState<RaceKey | null>(null);
    const [classe, setClasse] = useState<ClasseKey | null>(null);
    const [description, setDescription] = useState<string>("");

    const { mutate, isPending, error } = useMutation({
        mutationFn: async () => {
            if (!race || !classe || !description) return;
            return await axios.post("/api/player/create", { race, classe, description });
        },
    });

    return (
        <>
            <h2 className="text-center text-xl pt-6 px-4 text-foreground/80">Couch Campaign</h2>
            <h1 className="text-center text-3xl font-semibold pb-2 px-4">Character creation</h1>

            <div className="overflow-y-hidden grid mb-auto">
                <div className="flex flex-col p-4 overflow-y-hidden">
                    <div className="flex justify-between items-center gap-4">
                        <h1 className="text-xl">Name</h1>

                        <div className="flex gap-4 items-center">
                            <p>{userId}</p>
                            <Button onClick={logout} variant="ghost" size="sm">
                                Change
                            </Button>
                        </div>
                    </div>
                </div>

                <Separator />

                <div className="flex flex-col p-4 overflow-y-hidden">
                    <div className="flex justify-between items-center gap-4 mb-2">
                        <h1 className="text-xl">Race</h1>
                        {tab !== "race" && (
                            <Button onClick={() => setTab("race")} variant="ghost" size="sm">
                                Change
                            </Button>
                        )}
                    </div>

                    <AnimatePresence>
                        {tab === "race" ? (
                            <Card className="overflow-y-scroll divide-y py-2">
                                {Object.values(races).map((r) => (
                                    <RaceCard
                                        race={r}
                                        onSelect={(r) => {
                                            setRace(r);
                                            setTab(classe ? "desc" : "classe");
                                        }}
                                        key={r.name}
                                    />
                                ))}
                            </Card>
                        ) : (
                            race && (
                                <FadeDiv className="flex justify-between gap-4">
                                    <h1>{race}</h1>

                                    <p className="text-right text-sm">{races[race].description}</p>
                                </FadeDiv>
                            )
                        )}
                    </AnimatePresence>
                </div>

                <Separator />

                <div className="flex flex-col p-4 overflow-y-hidden">
                    <div className="flex justify-between items-center gap-4 mb-2">
                        <h1 className="text-xl">Class</h1>
                        {tab !== "classe" && (
                            <Button onClick={() => setTab("classe")} variant="ghost" size="sm">
                                Change
                            </Button>
                        )}
                    </div>

                    <AnimatePresence>
                        {tab === "classe" ? (
                            <Card className="overflow-y-scroll divide-y py-2">
                                {Object.values(classes).map((c) => (
                                    <ClasseCard
                                        classe={c}
                                        onSelect={(c) => {
                                            setClasse(c);
                                            setTab(race ? "desc" : "race");
                                        }}
                                        key={c.name}
                                    />
                                ))}
                            </Card>
                        ) : (
                            classe && (
                                <FadeDiv className="flex justify-between gap-4">
                                    <h1>{classe}</h1>

                                    <p className="text-right text-sm">{classes[classe].description}</p>
                                </FadeDiv>
                            )
                        )}
                    </AnimatePresence>
                </div>

                <Separator />

                <div className="flex flex-col p-4 overflow-y-hidden">
                    <div className="flex justify-between items-center gap-4  mb-2">
                        <h1 className="text-xl">Description</h1>
                        {tab !== "desc" && (
                            <Button onClick={() => setTab("desc")} variant="ghost" size="sm">
                                Change
                            </Button>
                        )}
                    </div>

                    <AnimatePresence>
                        {tab === "desc" && (
                            <FadeDiv>
                                <Label className="px-2 pb-0.5">
                                    Write a short description of your apperance and backstory
                                    <Textarea value={description} onChange={(e) => setDescription(e.target.value)} />
                                </Label>
                            </FadeDiv>
                        )}
                    </AnimatePresence>
                </div>
            </div>

            <div className="h-fit grid">
                {error && <p className="text-destructive">An error occured, please try again</p>}

                <Button
                    className="m-2"
                    size="lg"
                    onClick={() => mutate()}
                    disabled={isPending || !race || !classe || !description}
                >
                    {isPending && <LoaderCircle className="animate-spin" />}
                    Create character
                </Button>
            </div>
        </>
    );
}
