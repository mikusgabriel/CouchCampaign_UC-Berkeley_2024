import type { ClasseKey } from "@/lib/data/classes";
import type { RaceKey } from "@/lib/data/races";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { LoaderCircle } from "lucide-react";
import { useEffect, useState } from "react";

export default function CreatePage() {
    const [race, setRace] = useState<RaceKey | null>(null);
    const [classe, setClasse] = useState<ClasseKey | null>(null);
    const [description, setDescription] = useState<string>("");

    useEffect(() => {
        setRace("Elf");
        setClasse("Bard");
        setDescription("a tall long and young elf with a bow");
    });

    const { mutate, isPending, error } = useMutation({
        mutationFn: async () => {
            if (!race || !classe || !description) return;
            return await axios.post("/api/player/create", { race, classe, description });
        },
    });

    return (
        <div>
            <h1>Create your character</h1>

            <div>
                {error && <p>An error occured, try again</p>}

                <button onClick={mutate} disabled={isPending}>
                    {isPending && <LoaderCircle className="animate-spin" />}
                    Create
                </button>
            </div>
        </div>
    );
}
