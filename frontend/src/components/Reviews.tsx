import { reviews } from "../constants";
const Reviews = () => {
  return (
    <section id="reviews" className="px-4 md:px-10 lg:px-32 py-28">
      <div className="max-w-[80rem] mx-auto mb-24">
        <div className="relative">
          <p className="text-3xl md:text-6xl text-[#c8b0c9] text-right">
            Students' Reviews
          </p>
          <h2 className="text-4xl md:text-5xl text-[#754444] font-bold text-right mr-28 md:mr-[280px] mt-[-10px] z-20">
            學生評語
          </h2>
        </div>
      </div>
      <div className="max-w-[90rem] mx-auto">
        <ul className="flex flex-col md:grid grid-cols-3 gap-10">
          {reviews.map((reviewItem) => (
            <li className="diagonal p-10" key={reviewItem.id}>
              <div className="flex items-center gap-5 mb-7">
                <div className="w-[80px] h-[80px] bg-slate-400 rounded-full"></div>
                <p className="text-white text-xl font-bold">
                  {reviewItem.name}
                </p>
              </div>
              <p className="text-white text-xl">{reviewItem.content}</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
};

export default Reviews;
