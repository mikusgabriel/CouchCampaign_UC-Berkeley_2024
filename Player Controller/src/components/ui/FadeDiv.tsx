import { type Target, motion } from "framer-motion";
import * as React from "react";

const FadeDiv = React.forwardRef<
    React.ElementRef<typeof motion.div>,
    React.ComponentPropsWithoutRef<typeof motion.div>
>(({ initial, animate, exit, className, ...props }, ref) => (
    <motion.div
        initial={{ opacity: 0, height: 0, ...(initial as Target) }}
        animate={{ opacity: 1, height: "auto", ...(animate as Target) }}
        exit={{ opacity: 0, height: 0, ...(exit as Target) }}
        ref={ref}
        className={className}
        {...props}
    />
));
FadeDiv.displayName = "FadeDiv";

export { FadeDiv };
