import { Link } from "react-router-dom";
import { may } from "../constants";
import { Fragment } from "react/jsx-runtime";

//const AUTH_URL = 'http://example.com/api_admin/authorization'

const currentDate = new Date();
const currentMonth = currentDate.getMonth();
const currentYear = currentDate.getFullYear();
const today = currentDate.getDate();
const currentDay = `${currentYear}-${currentMonth + 1}-${today}`

const getCurrentMonthLessonsUrl = `/api_admin/get_lessons_for_a_month/${currentDay}`;

const AdminPanel = () => {
  

  const getCurrentMonthLessons = async () => {
    try {
      const request = new Request(getCurrentMonthLessonsUrl, {
        method: "GET",
        headers: {
          'Authorization': 'string',
        }
      })
      const response = await fetch(request)
      const data = await response.json()
      if (response.ok) {
        console.log(data)
      } else {
        // Обработка ошибки от сервера
        console.error("Request failed:", response.statusText);
        throw new Error();
      }    
    } catch (error) {
      console.error("Request error:", error);
    }
  }
  getCurrentMonthLessons();
  
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
      <Link to="/english-teacher-website" className="cursor-pointer my-5">
        ← Back to home page
      </Link>
      <div className="max-w-[90rem] mx-auto diagonal flex justify-center py-20">
        <table>
          <thead>
            <tr>
              <th className="w-[150px] h-[100px] text-center text-black">Date</th>
              <th className="w-[150px] h-[100px] text-center text-black">Time</th>
              <th className="w-[150px] h-[100px] text-center text-black">Name</th>
              <th className="w-[150px] h-[100px] text-center text-black">Email</th>
              <th className="w-[150px] h-[100px] text-center text-black">Phone</th>
              <th className="w-[150px] h-[100px] text-center text-black">Confirmation</th>
            </tr>
          </thead>
          <tbody>
            {may.map((day)=>(
              <Fragment key={day.id}>
                {day.lessons.map((lesson)=>(
                  <tr className="gradient-bg" key={lesson.id}>
                    <td className="w-[150px] h-[50px] text-center text-black">{day.date}</td>
                    <td className="w-[150px] h-[50px] text-center text-black">{lesson.selectedTime}</td>
                    <td className="w-[150px] h-[50px] text-center text-black">{lesson.lastName} {lesson.firstName}</td>
                    <td className="w-[150px] h-[50px] text-center text-black">{lesson.email}</td>
                    <td className="w-[150px] h-[50px] text-center text-black">{lesson.phone}</td>
                    <td className="w-[150px] h-[50px] text-center text-black">{lesson.confirmed ? "Yes" : "No"}</td>
                  </tr>                  
                ))}               
              </Fragment> 
            ))}  
          </tbody>                   
        </table>
      </div>
    </section>
  );
};

export default AdminPanel;
