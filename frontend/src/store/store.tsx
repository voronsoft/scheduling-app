import { makeAutoObservable } from "mobx";
import { createContext, useContext } from "react";
import { june } from "../constants";

interface lesson {
    id: number,
    email: string,
    firstName: string,
    lastName: string,
    phone: string,
    selectedDate: string,
    selectedTime: string,
    confirmed: boolean,
}

interface month {
    id: number,
    date: string,
    lessons:lesson[],
}

interface month {
    id: number,
    date: string,
    lessons:lesson[],
}

export class AdminStore {
    constructor() {
        makeAutoObservable(this);
    }

    currentMonthLessons:month[] = june;

    isCurrentMonthLessons:boolean = false;

    setIsCurrentMonthLessonsToTrue = () => {this.isCurrentMonthLessons = true};

    setCurrentMonthLessons = (data:month[]) => {this.currentMonthLessons = data};

    token: string = '';
    setToken = (newToken:string) => {
        this.token = newToken;
    }
}

export const AdminStoreContext = createContext<AdminStore | null>(null);

const useAdminStore = () => {
    const context = useContext(AdminStoreContext);
    if (context === null) {
        throw new Error(
            "You've forgotten to wrap your root component with AdminStoreProvider",
        );
    }
    return context;
}

const AdminStoreProvider = AdminStoreContext.Provider;


export { AdminStoreProvider, useAdminStore };