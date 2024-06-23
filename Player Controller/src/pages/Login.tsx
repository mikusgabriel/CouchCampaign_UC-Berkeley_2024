import useAuth from "@/lib/AuthContext";
import { LoaderCircle } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

export default function LoginPage() {
    const { loading, login } = useAuth();
    const [name, setName] = useState("");

    return (
        <div className="p-8 flex flex-col">
            <h1 className="text-center text-3xl font-semibold mb-4">Couch Campaign</h1>

            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    login(name);
                }}
                className="flex flex-col gap-4"
            >
                <Label>
                    Character's name
                    <Input value={name} onChange={(e) => setName(e.target.value)} />
                </Label>

                <Button variant="default" type="submit">
                    {loading && <LoaderCircle className="animate-spin" />}
                    Join game
                </Button>
            </form>
        </div>
    );
}
