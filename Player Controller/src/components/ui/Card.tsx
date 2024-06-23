import * as React from "react";

import { cn } from "@/lib/utils";

export interface CardProps extends React.TextareaHTMLAttributes<HTMLDivElement> {}

const Card = React.forwardRef<HTMLDivElement, CardProps>(({ className, ...props }, ref) => {
    return <div className={cn("flex flex-col bg-muted/20 rounded-sm", className)} ref={ref} {...props} />;
});
Card.displayName = "Card";

export { Card };
