import useStatus from "./lib/StatusContext";
import ChoicePage from "./pages/Choice";
import CreatePage from "./pages/Create";
import HomePage from "./pages/Home";
import LobbyPage from "./pages/Lobby";

function App() {
    const status = useStatus();

    if (status.status === "create") return <CreatePage />;
    if (status.status === "lobby") return <LobbyPage />;
    if (status.status === "choice") return <ChoicePage />;
    return <HomePage />;
}

export default App;
