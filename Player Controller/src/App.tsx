import useStatus from "./lib/StatusContext";
import { UserProvider } from "./lib/UserContext";
import CreatePage from "./pages/Create";
import HomePage from "./pages/Home";

function App() {
    const status = useStatus();

    if (status === "create") return <CreatePage />;

    return (
        <UserProvider>
            <HomePage />
        </UserProvider>
    );
}

export default App;
