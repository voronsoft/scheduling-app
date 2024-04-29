import { FormEvent, useState } from "react";
import FormInput from "./FormInput";
import { april } from "../constants";

const Schedule = () => {
  const currentDate = new Date();
  const currentMonth = currentDate.getMonth();
  const currentYear = currentDate.getFullYear();
  const today = currentDate.getDate();
  const months = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
  ];

  const [month, setMonth] = useState(currentMonth);
  const [year, setYear] = useState(currentYear);
  const [selectedDate, setSelectedDate] = useState(""); // Состояние для выбранной даты

  const currentMonthName = months[month];
  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const calendarData = [];
  let dayCounter = 1;
  let emptyCells = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;
  for (let i = 0; i < 6; i++) {
    const week = [];
    for (let j = 0; j < 7; j++) {
      if (emptyCells > 0) {
        week.push("");
        emptyCells--;
      } else if (dayCounter <= daysInMonth) {
        week.push(dayCounter);
        dayCounter++;
      } else {
        week.push("");
      }
    }
    calendarData.push(week);
    if (dayCounter > daysInMonth) break;
  }

  const handleDateSelect = (day: number | string) => {
    setSelectedDate(`${year}-${month + 1}-${day}`); // Форматирование даты в формат "гггг-мм-дд"
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const newClassRequest = Object.fromEntries(formData);

    // Это старый код формирования объекта для отправки. На всякий случай пока оставила:
    /* const formData = new FormData(event.currentTarget);
    const requestData = {};
    formData.forEach((value, key) => {
      const index = parseInt(key);
      requestData[index] = value; 
    });
    requestData["selectedDate"] = selectedDate; // Добавление выбранной даты в объект данных */

    try {
      const response = await fetch(
        "/api_calendar/receiving-data-from-the-calendar",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newClassRequest),
        }
      );

      if (response.ok) {
        // Обработка успешного ответа от сервера
        console.log("Request sent successfully!");
        // Очистить значения ввода в форме
        event.currentTarget.reset();
        setSelectedDate(""); // Сбросить выбранную дату
      } else {
        // Обработка ошибки от сервера
        console.error("Request failed:", response.statusText);
      }
    } catch (error) {
      // Обработка ошибок при выполнении запроса
      console.error("Request error:", error);
    }
  };

  return (
    <div className="md:grid grid-cols-2">
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
                className="w-[40px] h-[40px] text-center text-black"
              >
                {currentMonthName} {year}
              </th>
            </tr>
            <tr>
              <th className="w-[40px] h-[40px] text-center text-black">Пн</th>
              <th className="w-[40px] h-[40px] text-center text-black">Вт</th>
              <th className="w-[40px] h-[40px] text-center text-black">Ср</th>
              <th className="w-[40px] h-[40px] text-center text-black">Чт</th>
              <th className="w-[40px] h-[40px] text-center text-black">Пт</th>
              <th className="w-[40px] h-[40px] text-center text-black">Сб</th>
              <th className="w-[40px] h-[40px] text-center text-black">Вс</th>
            </tr>
          </thead>
          <tbody id="days">
            {calendarData.map((week) => {
              return (
                <tr>
                  {week.map((day) => {
                    const currentDay = `${year}-${month + 1}-${day}`;
                    const isDayBooked = april.some(
                      (element) => element.date === currentDay
                    );

                    return (
                      <td
                        className={`${
                          day === today && month === currentMonth
                            ? "today"
                            : "day"
                        }`}
                        style={{
                          color: `${isDayBooked ? "#ff0000" : "#ffffff"}`,
                        }}
                        onClick={() => {
                          handleDateSelect(day);
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

      <div className="form mt-8">
        <form
          id="appointmentForm"
          className="flex flex-col gap-5"
          autoComplete="off"
          onSubmit={(event) => {
            handleSubmit(event);
          }}
        >
          <FormInput
            id="name"
            type="text"
            name="firstName"
            placeholder="Имя"
            required
          />
          <FormInput
            id="surname"
            type="text"
            name="lastName"
            placeholder="Фамилия"
            required
          />
          <FormInput
            id="phone"
            type="tel"
            name="phone"
            placeholder="Телефон"
            required
          />
          <FormInput
            id="email"
            type="email"
            name="email"
            placeholder="Почта"
            required
          />
          <FormInput
            /* type="hidden" */
            name="selectedDate"
            id="selectedDate"
            value={selectedDate}
            required
          />
          <label htmlFor="time">Choose suitable time:</label>
          <select
            id="time"
            name="time"
            className="p-2 rounded-md text-black w-full"
          >
            <option value="15">3 pm</option>
            <option value="16">4 pm</option>
            <option value="17">5 pm</option>
            <option value="18">6 pm</option>
          </select>
          <button type="submit" className="bg-amber-400 p-2 rounded-md">
            Записаться
          </button>
        </form>
      </div>

      <div id="message" style={{ display: "none" }}></div>
    </div>
  );
};

export default Schedule;
