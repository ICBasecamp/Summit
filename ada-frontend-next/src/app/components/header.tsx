import { Tabs } from './tabs';
import { PlaceholdersAndVanishInputHeader } from './ticker-bar-header';

export const Header = () => {
    
    const tabs = [
        {
            title: "News",
            value: "1",
            content: <></>
        },
        {
            title: "Social Media",
            value: "2",
            content: <></>
        },
        {
            title: "Economic Indicators",
            value: "3",
            content: <></>
        },
        {
            title: "Earning Reports",
            value: "4",
            content: <></>
        },

    ]
    
    return (
        <div className="w-screen py-4 px-8 gap-2 flex flex-col">
            <div className="flex h-20 w-full items-center gap-2">
                <p className="font-semibold text-lg --font-geist-mono">Ice Climbers</p>
                <div className="flex w-1/2 items-center">
                    <PlaceholdersAndVanishInputHeader 
                        placeholders={['Search for a new ticker']}
                        onChange={() => {}}
                        onSubmit={() => {}}
                    />
                </div>
                <p className="ml-auto">Raw Data</p>
            </div>
            <Tabs tabs={tabs} />
        </div>
    )
}