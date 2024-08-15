import { useState, useEffect } from "react";
import { useAdminStore } from "../store/store";
import { observer } from "mobx-react-lite";
import { june } from "../constants";

const getCurrentMonthLessonsUrl = `/api_admin/lesson_dates_for_the_month_frontend`;

const Calendar = observer(() => {
  const store = useAdminStore();

  //Даты
  const localDate = new Date();
  const currentMonth = localDate.getMonth();
  const currentYear = localDate.getFullYear();
  const currentDay = localDate.getDate();

  const [month, setMonth] = useState(currentMonth);
  const [year, setYear] = useState(currentYear);
  //const [selectedDate, setSelectedDate] = useState("← Select a date"); // Состояние для выбранной даты

  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const totalDaysInMonth = new Date(year, month + 1, 0).getDate();

  //Названия месяцев
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const currentMonthName = months[month];

  //Создаем календарь
  const calendarData = store.createCalendar(firstDayOfMonth, totalDaysInMonth);

  useEffect(() => {
    try {
      store.fetchLessons(getCurrentMonthLessonsUrl);
      console.log(store.lessons);
    } catch (e: any) {
      console.log(e);
    }
  }, []);

  return (
    <div className="calendar">
      <div className=" w-[300px] flex justify-between">
        <button
          onClick={() => {
            setMonth(month - 1);
            if (month == 0) {
              setMonth(11);
              setYear(year - 1);
            }
          }}
        >
          Prev
        </button>
        <button
          onClick={() => {
            setMonth(month + 1);
            if (month == 11) {
              setMonth(0);
              setYear(year + 1);
            }
          }}
        >
          Next
        </button>
      </div>
      <table className="w-[300px]">
        <thead>
          <tr>
            <th
              colSpan={7}
              id="monthYear"
              className="w-[60px] h-[60px] text-center text-black"
            >
              {currentMonthName} {year}
            </th>
          </tr>
          <tr>
            <th className="w-[60px] h-[60px] text-center text-black">Mon</th>
            <th className="w-[60px] h-[60px] text-center text-black">Tue</th>
            <th className="w-[60px] h-[60px] text-center text-black">Wed</th>
            <th className="w-[60px] h-[60px] text-center text-black">Thur</th>
            <th className="w-[60px] h-[60px] text-center text-black">Fr</th>
            <th className="w-[60px] h-[60px] text-center text-black">St</th>
            <th className="w-[60px] h-[60px] text-center text-black">Sn</th>
          </tr>
        </thead>
        <tbody id="days">
          {calendarData.map((week) => {
            return (
              <tr>
                {week.map((day) => {
                  const currentFullDate = `${year}-${month + 1}-${day}`;
                  const isDayBooked = june.some(
                    (element) => element.date === currentFullDate
                  );

                  return (
                    <td
                      className={`${
                        day === currentDay && month === currentMonth
                          ? "today"
                          : "day"
                      }`}
                      style={{
                        color: `${isDayBooked ? "#ff0000" : "#ffffff"}`,
                      }}
                      onClick={() => {
                        store.setSelectedDate(day);
                      }}
                    >
                      {day}
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
});

export default Calendar;
