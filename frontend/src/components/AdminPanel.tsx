import { Link } from "react-router-dom";
import { Fragment } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { useAdminStore } from "../store/store";
import { observer } from "mobx-react-lite";


const date = new Date();
/* const currentMonth = date.getMonth() + 1;
const currentYear = date.getFullYear();
const today = date.getDate(); */
//const currentDate = `${currentYear}-${currentMonth}-${today}`;


//const getCurrentMonthLessonsUrl = `/api_admin/get_lessons_for_a_month/${currentDate}`;
//const getCurrentMonthLessonsUrl = `/api_admin/get_lessons_for_a_month/2024-6-01`;

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

const AdminPanel = observer(() => {
  const store = useAdminStore();

  const currentYear = date.getFullYear();
  const currentMonth = date.getMonth() + 1;
  const currentDay = date.getDate();

  const [error, setError] = useState();
  const [isLoading, setIsLoading] = useState(false);
  const [selectedYear, setSelectedYear]  = useState(currentYear);
  const [selectedMonth, setSelectedMonth] = useState(currentMonth);
  const [selectedDay, setSelectedDay] = useState(currentDay);

  const token = localStorage.getItem("token");



  const getPrevMonth = () => {
    const prevMonth = selectedMonth - 1;
    setSelectedMonth(prevMonth);
  }

  const getNextMonth = () => {
    const nextMonth = selectedMonth + 1;
    setSelectedMonth(nextMonth);
  }  
  
  const confirmLesson = (dayID:number, lessonID:number) => {
    console.log(dayID);
    console.log(lessonID);
  }

  useEffect(()=>{
    const getLessonsForProvidedDate = async () => {
      setIsLoading(true);
      console.log(store.token);
      try {
        const request = new Request(`/api_admin/get_lessons_for_a_month/${selectedYear}-${selectedMonth}-${selectedDay}`, {
          method: "GET",
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        })
        const response = await fetch(request)
        const data = await response.json() as month[];

        if (data.length > 0) {
          store.setIsCurrentMonthLessonsToTrue();
          store.setCurrentMonthLessons(data);
        } 
      } catch (e: any) {
        console.error("Request error:", e);
        setError(e);        
      } finally {
        setIsLoading(false);
      }
    }
    getLessonsForProvidedDate();
  }, [selectedDay, selectedMonth, selectedYear])

    
    if (isLoading) {
      return (
        <section id="reviews" className="px-4 md:px-10 lg:px-32 py-28">
        <div className="max-w-[80rem] mx-auto mb-24">
          <div className="relative">
            <p className="text-3xl md:text-6xl text-[#c8b0c9] text-right">
              Admin's Panel
            </p>
            <h2 className="text-4xl md:text-5xl text-[#754444] font-bold text-right mr-28 md:mr-[280px] mt-[-10px] z-20">
              控制面板
            </h2>
          </div>
        </div>      
        <div className="max-w-[90rem] mx-auto diagonal flex justify-center py-20">
          <Link to="/english-teacher-website" className="cursor-pointer my-5">
            Back to home page
          </Link>
          <div>Content is Loading...</div>
        </div>
      </section>
      )
    }

    if (error) {
      return (
        <section id="reviews" className="px-4 md:px-10 lg:px-32 py-28">
        <div className="max-w-[80rem] mx-auto mb-24">
          <div className="relative">
            <p className="text-3xl md:text-6xl text-[#c8b0c9] text-right">
              Admin's Panel
            </p>
            <h2 className="text-4xl md:text-5xl text-[#754444] font-bold text-right mr-28 md:mr-[280px] mt-[-10px] z-20">
              控制面板
            </h2>
          </div>
        </div>
        
        <div className="max-w-[90rem] mx-auto diagonal flex justify-center py-20">
          <Link to="/english-teacher-website" className="cursor-pointer my-5">
            Back to home page
          </Link>
          <div>Something went wrong, please reload the page</div>
        </div>
      </section>
      )
    }

    return (
      <section id="reviews" className="px-4 md:px-10 lg:px-32 py-28">
          <div className="max-w-[80rem] mx-auto mb-24">
          <div className="relative">
            <p className="text-3xl md:text-6xl text-[#c8b0c9] text-right">
              Admin's Panel
            </p>
            <h2 className="text-4xl md:text-5xl text-[#754444] font-bold text-right mr-28 md:mr-[280px] mt-[-10px] z-20">
              控制面板
            </h2>
          </div>
        </div>
        
        <div className="max-w-[90rem] mx-auto diagonal flex flex-col justify-center py-32 px-20 gap-10">
          <Link to="/english-teacher-website" className="cursor-pointer text-white">
          Return to home page
          </Link>
          <div className="arrows flex gap-3">
            <button onClick={()=>{getPrevMonth()}}>Back</button>
            <button onClick={()=>{getNextMonth()}}>Forward</button>
          </div>
          {store.isCurrentMonthLessons ? <table>
            <thead>
              <tr>
                <th className="w-[150px] h-[100px] text-center text-black">Date</th>
                <th className="w-[150px] h-[100px] text-center text-black">Time</th>
                <th className="w-[150px] h-[100px] text-center text-black">Name</th>
                <th className="w-[150px] h-[100px] text-center text-black">Email</th>
                <th className="w-[150px] h-[100px] text-center text-black">Phone</th>
                <th className="w-[150px] h-[100px] text-center text-black">Confirmation</th>
                <th className="w-[150px] h-[100px] text-center text-black">Confirm</th>
                <th className="w-[150px] h-[100px] text-center text-black">Edit</th>
                <th className="w-[150px] h-[100px] text-center text-black">Delete</th>
              </tr>
            </thead>
            <tbody>
              {store.currentMonthLessons.map((day)=>(
                <Fragment key={day.id}>
                  {day.lessons.map((lesson)=>(
                    <tr className="gradient-bg" key={lesson.id}>
                      <td className="w-[150px] h-[50px] text-center text-black">{day.date}</td>
                      <td className="w-[150px] h-[50px] text-center text-black">{lesson.selectedTime}</td>
                      <td className="w-[150px] h-[50px] text-center text-black">{lesson.lastName} {lesson.firstName}</td>
                      <td className="w-[150px] h-[50px] text-center text-black">{lesson.email}</td>
                      <td className="w-[150px] h-[50px] text-center text-black">{lesson.phone}</td>
                      <td className="w-[150px] h-[50px] text-center text-black">{lesson.confirmed ? "Yes" : "No"}</td>
                      <td className="w-[150px] h-[50px] text-center text-black">{lesson.confirmed ? null : <button className="button_admin" onClick={()=>{confirmLesson(day.id, lesson.id)}}>Confirm</button>}</td>
                      <td className="w-[150px] h-[50px] text-center text-black"><button className="button_admin">Edit</button></td>
                      <td className="w-[150px] h-[50px] text-center text-black"><button className="button_delete">Delete</button></td>
                    </tr>                  
                  ))}              
                </Fragment>
              ))}  
            </tbody> 
            </table> : <div>No Lessons Booked for this month</div>
          }
        </div>      
      </section>
    );
  }
); 


export default AdminPanel;
