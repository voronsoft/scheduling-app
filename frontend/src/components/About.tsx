import { experience } from "../constants";

const About = () => {
  return (
    <section id="about" className="diagonal px-4 md:px-10 lg:px-32 py-20">
      <div className="max-w-[80rem] mx-auto">
        <div className="relative pb-10">
          <p className="text-3xl md:text-6xl text-[#ffffff6e] text-right">
            {experience.headerEng}
          </p>
          <h2 className="text-4xl md:text-5xl text-[#754444] font-bold text-right mr-24 md:mr-[280px] mt-[-10px] z-20">
            {experience.headerCn}
          </h2>
        </div>
        <div className="flex flex-col gap-5 md:gap-0 md:grid grid-cols-2 md:mb-10">
          <div className="w-full h-[100%]">
            <p className="m-0 p-0 text-white text-9xl md:text-[10rem] leading-none text-right font-noto font-bold">
              {experience.word1}
            </p>
          </div>
          <p className="text-white font-inter text-xl mb-5 max-w-[600px] mr-0 ml-auto">
            {experience.paragraph1}
          </p>
        </div>
        <div className="flex flex-col-reverse gap-5 md:gap-0 md:grid grid-cols-2 md:mb-10">
          <p className="text-white font-inter text-xl mb-5 max-w-[600px]">
            {experience.paragraph2}
          </p>
          <p className="m-0 p-0 text-white text-9xl md:text-[10rem] leading-none font-noto font-bold">
            {experience.word2}
          </p>
        </div>
        <div className="flex flex-col gap-5 md:gap-0 md:grid grid-cols-2">
          <p className="m-0 p-0 text-white text-9xl md:text-[10rem] leading-none text-right font-noto font-bold">
            {experience.word3}
          </p>
          <p className="text-white font-inter text-xl mb-5 max-w-[600px] mr-0 ml-auto">
            {experience.paragraph3}
          </p>
        </div>
      </div>
    </section>
  );
};

export default About;
