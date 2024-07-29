import { createContext, useContext } from "react";


export const ModalContext = createContext<string | undefined>(undefined);

export function useModalContext () {
    const token = useContext(ModalContext);
    if (token === undefined) {
        throw new Error("useModalContext must be used with a ModalContext");
    }
    return token;
}