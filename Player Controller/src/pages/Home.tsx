import useAuth from "@/lib/AuthContext";
import useUser from "@/lib/UserContext";
import { LoaderCircle } from "lucide-react";

export default function HomePage() {
    const { loading, logout } = useAuth();
    const user = useUser();

    return (
        <div>
            <h1>Home</h1>

            <p>{user.name}</p>

            <button onClick={() => logout()}>
                {loading && <LoaderCircle className="animate-spin" />}
                Log out
            </button>
        </div>
    );
}
