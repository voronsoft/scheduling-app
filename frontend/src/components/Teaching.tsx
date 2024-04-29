import { advantages } from "../constants";

const Teaching = () => {
  return (
    <section id="teaching" className="px-4 md:px-10 lg:px-32 py-28">
      <div className="max-w-[80rem] mx-auto mb-24">
        <div className="relative">
          <p className="text-3xl md:text-6xl text-[#c8b0c9] text-right">
            Teaching style
          </p>
          <h2 className="text-4xl md:text-5xl text-[#754444] font-bold text-right mr-28 md:mr-[280px] mt-[-10px] z-20">
            教學方式
          </h2>
        </div>
      </div>
      <div className="max-w-[90rem] mx-auto">
        <ul className="grid md:grid-cols-2 gap-5">
          {advantages.map((advantage) => (
            <li
              className="shadow-xl rounded-3xl p-5 grid grid-cols-2 sm:max-w-[400px] md:max-w-none sm:mx-auto md:mx-0 md:flex md:gap-5"
              key={advantage.id}
            >
              <div className="w-[100px]">
                <img
                  src={advantage.img}
                  className="w-[100px]"
                  alt="study icon"
                />
              </div>
              <div>
                <h3 className="text-2xl font-bold mb-4">{advantage.title}</h3>
                <p className="text-xl">{advantage.content}</p>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
};

export default Teaching;
