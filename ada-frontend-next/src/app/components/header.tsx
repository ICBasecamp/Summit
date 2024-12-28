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
        <div className="w-full px-8 gap-2 flex flex-col">
            <div className="bg-zinc-800 flex h-20 w-full items-center gap-2">
                <p>Logo goes here</p>
                <div className="flex w-1/2 items-center">
                    <PlaceholdersAndVanishInputHeader 
                        placeholders={['Search for a new ticker']}
                        onChange={() => {}}
                        onSubmit={() => {}}
                    />
                </div>
            </div>
            <Tabs tabs={tabs} />
        </div>
    )
}