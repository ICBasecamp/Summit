import { ReturnValue } from "use-count-up"

interface ProgressBarProps {
    value: number | ReturnValue;
    colour?: string;
}

export const ProgressBar = ({ value, colour = 'bg-blue-600' }: ProgressBarProps) => {
    return (
        <div className="flex items-center gap-x-3 whitespace-nowrap w-full">
            <div className="flex w-full h-2 bg-gray-200 rounded-full overflow-hidden dark:bg-neutral-700" role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={100}>
                <div className={`flex flex-col justify-center rounded-full overflow-hidden text-xs text-white text-center whitespace-nowrap transition duration-500 ${colour}`} style={{width: `${value}%`}}></div>
            </div>
            <div className="flex items-center text-end">
                <span className="text-sm text-white">{value}%</span>
            </div>
        </div>
    )
}