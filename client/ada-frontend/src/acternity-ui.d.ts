declare module 'aceternity-ui' {
    import { FC, ChangeEvent, FormEvent } from 'react';
  
    interface PlaceholdersAndVanishInputProps {
      placeholders: string[];
      onChange: (e: ChangeEvent<HTMLInputElement>) => void;
      onSubmit: (e: FormEvent<HTMLFormElement>) => void;
    }
  
    export const PlaceholdersAndVanishInput: FC<PlaceholdersAndVanishInputProps>;
  }