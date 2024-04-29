import Schedule from "./Schedule";

const Calendar = () => {
  return (
    <section id="trial" className="diagonal px-4 md:px-10 lg:px-32 py-28">
      <div className="max-w-[80rem] mx-auto mb-10 md:mb-24">
        <div className="relative">
          <p className="text-3xl md:text-6xl text-[#e1c1e2] text-right">
            My Schedule
          </p>
          <h2 className="text-4xl md:text-5xl text-[#754444] font-bold text-right mr-24 md:mr-[280px] mt-[-10px] z-20">
            我的時間表
          </h2>
        </div>
      </div>
      <div className="max-w-[80rem] mx-auto">
        <div className="text-white flex-1 text-xl">
          <h3 className="text-amber-400 text-4xl md:text-5xl font-bold pr-3 font-inter mb-10">
            聯機安排上課
          </h3>
          <Schedule />
        </div>
      </div>
    </section>
  );
};

export default Calendar;
