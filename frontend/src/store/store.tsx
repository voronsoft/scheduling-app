import { makeAutoObservable } from "mobx";
import { createContext, useContext } from "react";
import { june } from "../constants";

export interface lesson {
    id: number,
    email: string,
    firstName: string,
    lastName: string,
    phone: string,
    selectedDate: string,
    selectedTime: string,
    confirmed: boolean,
}

export interface month {
    id: number,
    date: string,
    lessons:lesson[],
}

export class AdminStore {
    constructor() {
        makeAutoObservable(this);
    }

    date = new Date();
    currentYear = this.date.getFullYear();
    currentMonth = this.date.getMonth();
    currentDay = this.date.getDate();

    createCalendar = (firstDay:number, totalDays:number) => {
        let calendarArray:((string | number)[])[] = [];
        let dayCounter = 1;
        let emptyCells = firstDay === 0 ? 6 : firstDay - 1;

        for (let i = 0; i < 6; i++) {
            const week:(number | string)[] = [];

            for (let j = 0; j < 7; j++) {
            if (emptyCells > 0) {
                week.push("");
                emptyCells--;
            } else if (dayCounter <= totalDays) {
                week.push(dayCounter);
                dayCounter++;
            } else {
                week.push("");
            }
            }
            calendarArray.push(week);
            if (dayCounter > totalDays) break;
        }
        return calendarArray;
    }

    selectedDate: string = `${this.currentYear}-${this.currentMonth}-${this.currentDay}`;
    
    setSelectedDate = (day:number | string) => {
        this.selectedDate = `${this.currentYear}-${this.currentMonth}-${day}`;
    }

    currentMonthLessons:month[] = june;

    isCurrentMonthLessons:boolean = false;

    setIsCurrentMonthLessonsToTrue = () => {this.isCurrentMonthLessons = true};

    setCurrentMonthLessons = (data:month[]) => {this.currentMonthLessons = data};
    lessons: lesson[] = [];
    lessonError: any = '';
    
    async fetchLessons (apiAddress:string) {
        const response = await fetch(`${apiAddress}/${this.currentYear}-${this.currentMonth + 1}-1`);
        const lessonsFromServer = (await response.json() as lesson[]);
        if (response.ok) {
            this.lessons = lessonsFromServer;
        } else {
            this.lessonError = response.statusText;
            console.log(`This is an error: ${this.lessonError}`);            
        }
    };

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