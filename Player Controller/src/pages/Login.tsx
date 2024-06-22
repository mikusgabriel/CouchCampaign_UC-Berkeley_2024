import useAuth from "@/lib/AuthContext";
import { LoaderCircle } from "lucide-react";

export default function LoginPage() {
    const { loading, login } = useAuth();

    return (
        <div>
            <h1>Couch Campaign</h1>

            <button onClick={() => login("guibi")}>
                {loading && <LoaderCircle className="animate-spin" />}
                Login
            </button>
        </div>
    );
}
