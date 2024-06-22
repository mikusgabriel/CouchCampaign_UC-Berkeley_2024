import type { Classe, ClasseKey } from "@/lib/data/classes";
import type { Race, RaceKey } from "@/lib/data/races";
import { Button } from "./ui/Button";
import { FadeDiv } from "./ui/FadeDiv";

export function RaceCard({
    race,
    onSelect,
    button,
}: { race: Race; onSelect: (name: RaceKey) => void; button?: string }) {
    return (
        <FadeDiv>
            <div className="mb-1 px-4 py-2 gap-1 flex flex-col">
                <div className="flex justify-between items-center w-full">
                    <h1 className="text-lg">{race.name}</h1>
                </div>

                <div className="flex justify-between items-center w-full gap-4">
                    <h2 className="text-sm">{race.description}</h2>
                    <Button onClick={() => onSelect(race.name)} size="sm">
                        {button ?? "Select"}
                    </Button>
                </div>
            </div>
        </FadeDiv>
    );
}

export function ClasseCard({
    classe,
    onSelect,
    button,
}: { classe: Classe; onSelect: (name: ClasseKey) => void; button?: string }) {
    return (
        <FadeDiv>
            <div className="mb-1 px-4 py-2 gap-1 flex flex-col">
                <div className="flex justify-between items-center w-full">
                    <h1 className="text-lg">{classe.name}</h1>
                </div>

                <div className="flex justify-between items-center w-full gap-4">
                    <h2 className="text-sm">{classe.description}</h2>
                    <Button onClick={() => onSelect(classe.name)} size="sm">
                        {button ?? "Select"}
                    </Button>
                </div>
            </div>
        </FadeDiv>
    );
}
