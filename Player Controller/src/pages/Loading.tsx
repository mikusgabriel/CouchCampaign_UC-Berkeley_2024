import { LoaderCircle } from "lucide-react";

export default function LoadingPage() {
    return (
        <div className="flex items-center justify-center gap-4 text-xl flex-1">
            <LoaderCircle className="animate-spin" />
            Loading
        </div>
    );
}
