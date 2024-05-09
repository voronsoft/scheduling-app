import {
  heroDesktop,
  heroTablet,
  heroFull,
  teacherGongBig,
  teacherGongSm,
  studyMode,
  selfTest,
  confidence,
  speed,
  vocab,
} from "../assets";

export const navLinks = [
  {
    id: "about",
    title: "我的經驗",
  },
  {
    id: "reviews",
    title: "學生評論",
  },
  {
    id: "trial",
    title: " 預定試教",
  },
  {
    id: "teaching",
    title: "我的教育概念",
  },
];

export const loginLinks = [
  {
    id: "login",
    title: "Log In",
  },
  {
    id: "logout",
    title: "Log Out",
  },
];

export const heroSection = {
  id: "hero",
  photoSmall: teacherGongSm,
  photoBig: teacherGongBig,
  teacherName: "STEVEN 龔少",
  tagline: "英文家教老師",
  phoneLink: "tel:0987-988258",
  phone: "0987-988258",
  lineLink: "https://msng.link/o?luvwinnie7969=ln",
  line: "luvwinnie7969",
  backgroundSmall: heroTablet,
  backgroundLarge: heroDesktop,
  backgroundXL: heroFull,
};

export const experience = {
  headerEng: "My experience",
  headerCn: "我的經驗",
  word1: "興趣",
  paragraph1:
    "記共前野敗顔移名察明課念話朝載提室。展何上作動学囲勤岡子抗判。初年余皇動経左点活内連百分崎星府万。食直月車家映摘信車醸代契可番禁交乗。能近説面災英木数放質試理値図図。検初大覧化更打条数今家起支衡松。性紅益入直社出傑碁応吉収身超文。集人能解定万勢芸株政傳宏産。誉機香法本兄詳四雇上趣暮止玲。掲購容収作残勢国数動決豊朝回場。",
  word2: "努力",
  paragraph2:
    "記共前野敗顔移名察明課念話朝載提室。展何上作動学囲勤岡子抗判。初年余皇動経左点活内連百分崎星府万。食直月車家映摘信車醸代契可番禁交乗。能近説面災英木数放質試理値図図。検初大覧化更打条数今家起支衡松。性紅益入直社出傑碁応吉収身超文。集人能解定万勢芸株政傳宏産。誉機香法本兄詳四雇上趣暮止玲。掲購容収作残勢国数動決豊朝回場。",
  word3: "認真",
  paragraph3:
    "報局趣結戸更信別待更毎見変多年慢正課。否演同提真秒際攻並重軟茶選校認測断願自年。文線昭買写底余番少治生野帰。問星整所作判円円界無放化改禁州注夜考。軍文樹対方稿究社将蝶算見庁救。露育万原変演鈴加発職天抗迷通松時。決岸報載勢話支際題磨義燃文報情条雄目。市安説有長一型短光抜交回重演。約愛目訴記案何制近途殺週属共悩供来納。",
};

export const reviews = [
  {
    id: "review 1",
    name: "王一博",
    content:
      "記共前野敗顔移名察明課念話朝載提室。展何上作動学囲勤岡子抗判。初年余皇動経左点活内連百分崎星府万。",
  },
  {
    id: "review 2",
    name: "羅雲熙",
    content:
      "決岸報載勢話支際題磨義燃文報情条雄目。市安説有長一型短光抜交回重演。約愛目訴記案何制近途殺週属共悩供来納。",
  },
  {
    id: "review 3",
    name: "龚俊",
    content:
      "記共前野敗顔移名察明課念話朝載提室。展何上作動学囲勤岡子抗判。初年余皇動経左点活内連百分崎星府万。",
  },
];

export const advantages = [
  {
    id: "adv 1",
    img: studyMode,
    title: "學習模式",
    content: "反覆的英文對談加上中翻英訓練",
  },
  {
    id: "adv 2",
    img: selfTest,
    title: "檢驗成效的方法",
    content: "每次英語對談都可自行檢驗",
  },
  {
    id: "adv 3",
    img: confidence,
    title: "學習信心",
    content: "越常講英文，英語能力必定越提升，信心也會隨之增加",
  },
  {
    id: "adv 4",
    img: speed,
    title: "學習速度",
    content:
      "初期學習速度雖較慢，但單字不易忘，文法觀念也具系統性，在後期能培養出強烈語感，學習速度也隨之加快",
  },
  {
    id: "adv 5",
    img: vocab,
    title: "背單子",
    content:
      "照音拼字，並知道那些單字無法對應中文，在學習中可大幅降低被中文干擾的狀況",
  },
];

export const lessons: {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  phone: string;
  selectedDate: string;
  selectedTime: string;
  confirmed: boolean;
}[] = [
  {
    id: 1,
    email: "felix@gmail.com",
    firstName: "Felix",
    lastName: "Lee",
    phone: "89115555555",
    selectedDate: "2024-5-14",
    selectedTime: "18:00",
    confirmed: false,
  },
  {
    id: 2,
    email: "woo@gmail.com",
    firstName: "Wooyoung",
    lastName: "Jung",
    phone: "89117777777",
    selectedDate: "2024-6-23",
    selectedTime: "18:00",
    confirmed: false,
  },
  {
    id: 3,
    email: "hwa@gmail.com",
    firstName: "Seonghwa",
    lastName: "Park",
    phone: "89113333333",
    selectedDate: "2024-5-1",
    selectedTime: "18:00",
    confirmed: false,
  },
  {
    id: 4,
    email: "joong@gmail.com",
    firstName: "Hongjoong",
    lastName: "Kim",
    phone: "89111111111",
    selectedDate: "2024-4-30",
    selectedTime: "17:00",
    confirmed: true,
  },
  {
    id: 5,
    email: "san@gmail.com",
    firstName: "San",
    lastName: "Choi",
    phone: "89112222222",
    selectedDate: "2024-4-30",
    selectedTime: "15:00",
    confirmed: true,
  },
];

export const may = [
  {
    id: 1,
    date: "2024-5-28",
    lessons: [
      {
        id: 1,
        email: "joong@gmail.com",
        firstName: "Hongjoong",
        lastName: "Kim",
        phone: "89111111111",
        selectedDate: "2024-5-28",
        selectedTime: "15:00",
        confirmed: true,
      },
      {
        id: 2,
        email: "san@gmail.com",
        firstName: "San",
        lastName: "Choi",
        phone: "89112222222",
        selectedDate: "2024-5-28",
        selectedTime: "17:00",
        confirmed: true,
      },
    ],
  },
  {
    id: 2,
    date: "2024-5-29",
    lessons: [
      {
        id: 1,
        email: "woo@gmail.com",
        firstName: "Wooyoung",
        lastName: "Jung",
        phone: "89117777777",
        selectedDate: "2024-5-29",
        selectedTime: "18:00",
        confirmed: true,
      },
    ],
  },
  {
    id: 3,
    date: "2024-5-30",
    lessons: [
      {
        id: 1,
        email: "felix@gmail.com",
        firstName: "Felix",
        lastName: "Lee",
        phone: "89115555555",
        selectedDate: "2024-5-30",
        selectedTime: "16:00",
        confirmed: false,
      },
      {
        id: 2,
        email: "hyunjin@gmail.com",
        firstName: "Hyunjin",
        lastName: "Hwang",
        phone: "89110000000",
        selectedDate: "2024-5-30",
        selectedTime: "17:00",
        confirmed: true,
      },
    ],
  },
];
