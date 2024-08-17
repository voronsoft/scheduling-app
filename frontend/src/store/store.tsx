import { makeAutoObservable } from "mobx";
import { createContext, useContext } from "react";
import { june } from "../constants";
import { getLessonsForMonth } from "../api/lessonsForCurrentMonth";

export interface lesson {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  phone: string;
  selectedDate: string;
  selectedTime: string;
  confirmed: boolean;
}

export interface month {
  id: number;
  date: string;
  lessons: lesson[];
}

export interface lessonPerDay {
  date: string;
  lessons: number[];
}

export class AdminStore {
  constructor() {
    makeAutoObservable(this);
  }

  date = new Date();
  currentYear = this.date.getFullYear();
  currentMonth = this.date.getMonth();
  currentDay = this.date.getDate();

  createCalendar = (firstDay: number, totalDays: number) => {
    let calendarArray: (string | number)[][] = [];
    let dayCounter = 1;
    let emptyCells = firstDay === 0 ? 6 : firstDay - 1;

    for (let i = 0; i < 6; i++) {
      const week: (number | string)[] = [];

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
  };

  selectedDate: string = `${this.currentYear}-${this.currentMonth + 1}-${
    this.currentDay
  }`;

  setSelectedDate = (day: number | string) => {
    this.selectedDate = `${this.currentYear}-${this.currentMonth + 1}-${day}`;
  };

  addMonth = (month: number, year: number) => {
    this.currentMonth = month + 1;
    if (month == 11) {
      this.addYear(year);
    }
  };

  addYear = (year: number) => {
    this.currentYear = year + 1;
  };

  substractMonth = (month: number, year: number) => {
    this.currentMonth = month - 1;
    if (month == 0) {
      this.substractYear(year);
    }
  };

  substractYear = (year: number) => {
    this.currentYear = year - 1;
  };

  currentMonthLessons: month[] = june;

  isCurrentMonthLessons: boolean = false;

  setIsCurrentMonthLessonsToTrue = () => {
    this.isCurrentMonthLessons = true;
  };

  setCurrentMonthLessons = (data: month[]) => {
    this.currentMonthLessons = data;
  };

  formatData = (data: month[]) => {
    const newArray = data.map((element) => {
      const array = element.date.split("-");
      if (array[1].charAt(0) === "0") {
        const newMonth = array[1].slice(1);
        array[1] = newMonth;
      }
      if (array[2].charAt(0) === "0") {
        const newDay = array[2].slice(1);
        array[2] = newDay;
      }
      const newDate = `${array[0]}-${array[1]}-${array[2]}`;
      return { ...element, date: newDate };
    });

    return newArray;
  };

  async loadLessons() {
    const response = await getLessonsForMonth(
      this.currentYear,
      this.currentMonth + 1
    );
    const formattedResponse = this.formatData(response);
    console.log(formattedResponse);
    this.setCurrentMonthLessons(formattedResponse);
  }
}

export const AdminStoreContext = createContext<AdminStore | null>(null);

const useAdminStore = () => {
  const context = useContext(AdminStoreContext);
  if (context === null) {
    throw new Error(
      "You've forgotten to wrap your root component with AdminStoreProvider"
    );
  }
  return context;
};

const AdminStoreProvider = AdminStoreContext.Provider;

export { AdminStoreProvider, useAdminStore };
