import { useEffect, useState } from "react";
//import FormInput from "./FormInput";
import { may } from "../constants";
import { SubmitHandler, useForm } from "react-hook-form";

type FormFields = {
  name: string;
  surname: string;
  phone: string;
  email: string;
  selectedDate: string;
  time: string;
};

const Schedule = () => {
  const {
    register,
    reset,
    setValue,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<FormFields>();
  const currentDate = new Date();
  const currentMonth = currentDate.getMonth();
  const currentYear = currentDate.getFullYear();
  const today = currentDate.getDate();
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

  const [month, setMonth] = useState(currentMonth);
  const [year, setYear] = useState(currentYear);
  const [selectedDate, setSelectedDate] = useState("← Select a date"); // Состояние для выбранной даты

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

  useEffect(() => {
    setValue("selectedDate", selectedDate, {
      shouldValidate: true,
      shouldDirty: true,
      shouldTouch: true,
    });
  }, [selectedDate]);

  const handleDateSelect = (day: number | string) => {
    setSelectedDate(`${year}-${month + 1}-${day}`); // Форматирование даты в формат "гггг-мм-дд"
  };

  const onSubmit: SubmitHandler<FormFields> = async (data) => {
    console.log(data);

    try {
      const response = await fetch(
        "/api_calendar/receiving-data-from-the-calendar",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
      );
      if (response.ok) {
        // Обработка успешного ответа от сервера
        console.log("Request sent successfully!");
        // Очистить значения ввода в форме
        reset(); // Сбросить форму
      } else {
        // Обработка ошибки от сервера
        console.error("Request failed:", response.statusText);
        throw new Error();
      }
    } catch (error) {
      // Обработка ошибок при выполнении запроса
      console.error("Request error:", error);
      setError("root", {
        message: "Something went wrong, please refresh the page and try again",
      });
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
                    const currentDay = `${year}-${month + 1}-${day}`;
                    const isDayBooked = may.some(
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
          onSubmit={handleSubmit(onSubmit)}
        >
          <input
            {...register("name", { required: "Please enter your name" })}
            type="text"
            placeholder="Name"
            className="p-2 rounded-md text-black w-full"
          />
          {errors.name && (
            <div className="text-red-500">{errors.name.message}</div>
          )}
          <input
            {...register("surname", { required: "Please enter your surname" })}
            type="text"
            placeholder="Surname"
            className="p-2 rounded-md text-black w-full"
          />
          {errors.surname && (
            <div className="text-red-500">{errors.surname.message}</div>
          )}
          <input
            {...register("phone", {
              required: "Please enter a valid phone number",
              pattern: /^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$/,
            })}
            type="tel"
            placeholder="Phone"
            className="p-2 rounded-md text-black w-full"
          />
          {errors.phone && (
            <div className="text-red-500">{errors.phone.message}</div>
          )}
          <input
            {...register("email", {
              required: "Please enter a valid email",
              pattern: /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/,
            })}
            type="email"
            placeholder="Email"
            className="p-2 rounded-md text-black w-full"
          />
          {errors.email && (
            <div className="text-red-500">{errors.email.message}</div>
          )}
          <input
            {...register("selectedDate", {
              required: "Please choose a preferable date in the calendar",
            })}
            readOnly
            name="selectedDate"
            type="text"
            placeholder="Select a date"
            className="p-2 rounded-md text-black w-full"
          />
          {errors.selectedDate && (
            <div className="text-red-500">{errors.selectedDate.message}</div>
          )}

          <label htmlFor="time">Choose suitable time:</label>
          <select
            {...register("time", {
              required: "Please choose your most suitable time",
            })}
            id="time"
            name="time"
            className="p-2 rounded-md text-black w-full"
          >
            <option value="15">3 pm</option>
            <option value="16">4 pm</option>
            <option value="17">5 pm</option>
            <option value="18">6 pm</option>
          </select>
          {errors.time && (
            <div className="text-red-500">{errors.time.message}</div>
          )}
          <button
            type="submit"
            disabled={isSubmitting}
            className="bg-amber-400 p-2 rounded-md"
          >
            {isSubmitting ? "Loading" : "Submit"}
          </button>
        </form>
      </div>

      <div id="message" style={{ display: "none" }}></div>
    </div>
  );
};

export default Schedule;
