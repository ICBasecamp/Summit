import { PlaceholdersAndVanishInputHeader } from './ticker-bar-header';

export const Header = () => (
    <div className="bg-zinc-800 flex h-20 w-full items-center px-8 gap-2">
        <p>Logo goes here</p>
        <div className="flex w-1/2 items-center">
        <PlaceholdersAndVanishInputHeader 
            placeholders={['Search for a new ticker']}
            onChange={() => {}}
            onSubmit={() => {}}
            />
        </div>
     </div>
)