import { heroSection } from "../constants";

const Contacts = () => {
  return (
    <section id="trial" className="diagonal px-4 md:px-10 lg:px-32 py-28">
      <div className="max-w-[80rem] mx-auto mb-10 md:mb-24">
        <div className="relative">
          <p className="text-3xl md:text-6xl text-[#e1c1e2] text-right">
            Book a Trial
          </p>
          <h2 className="text-4xl md:text-5xl text-[#754444] font-bold text-right mr-28 md:mr-[280px] mt-[-10px] z-20">
            預定試教
          </h2>
        </div>
      </div>
      <div className="max-w-[80rem] mx-auto">
        <ul className="flex flex-col md:flex-row md:gap-10">
          <li className="relative self-end">
            <div className=" bg-amber-400 circle">
              <a href={heroSection.phoneLink}>
                <p className="text-xl text-center">
                  馬上預定
                  <br />
                  免費試教!
                </p>
              </a>
            </div>
          </li>
          <li className="text-white flex-1 text-xl">
            <h3 className="text-amber-400 text-4xl md:text-5xl font-bold pr-3 font-inter mb-10">
              預定免費試教
            </h3>
            <p className="text-white text-xl inline-block">
              記共前野敗顔移名察明課念話朝載提室。展何上作動学囲勤岡子抗判。初年余皇動経左点活内連百分崎星府万。食直月車家映摘信車醸代契可番禁交乗。能近説面災英木数放質試理値図図。検初大覧化更打条数今家起支衡松。性紅益入直社出傑碁応吉収身超文。集人能解定万勢芸株政傳宏産。誉機香法本兄詳四雇上趣暮止玲。掲購容収作残勢国数動決豊朝回場。
            </p>
          </li>
        </ul>
      </div>
    </section>
  );
};

export default Contacts;
