import { ReturnValue } from "use-count-up";

interface CircularProgressProps {
    value: ReturnValue | number;
    className?: string;
    colour?: string;
    textColour?: string;
}

export const CircularProgress = ({ value, className, colour, textColour }: CircularProgressProps) => {
    return (
        <div className={`relative size-40 ${className}`}>
            <svg className="size-full -rotate-90" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
                <circle cx="18" cy="18" r="16" fill="none" className="stroke-current text-gray-200 dark:text-neutral-700" strokeWidth="2"></circle>
                <circle cx="18" cy="18" r="16" fill="none" className={`stroke-current text-blue-600 dark:text-blue-500 ${colour}`} strokeWidth="2" strokeDasharray="100" strokeDashoffset={100 - value} strokeLinecap="round"></circle>
            </svg>

            <div className="absolute top-1/2 start-1/2 transform -translate-y-1/2 -translate-x-1/2">
                <span className={`text-center text-2xl font-bold text-white ${textColour}`}>{value}%</span>
            </div>
        </div>
    );
}