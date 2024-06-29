
import { useState } from "react";
import { motion } from "framer-motion";
import Links from "./Links";
import ToggleButton from "./ToggleButton";

const variants = {
  open: {
    clipPath: "circle(1400px at 40px 40px)",
    transition: {
      type: "spring",
      stiffness: 20,
    },
  },
  closed: {
    clipPath: "circle(30px at 40px 40px)",
    transition: {
      delay: 0.5,
      type: "spring",
      stiffness: 400,
      damping: 40,
    },
  },
};

const Navbar = () => {
  const [open, setOpen] = useState<boolean>(false);

  return (
    <motion.nav
      className="bg-[#8865A9] text-black flex flex-col place-items-center"
      animate={open ? "open" : "closed"}
    >
      <motion.div
        className="bg-[#8865A9] w-[100%] md:w-[400px] fixed top-0 left-0 bottom-0 z-40"
        variants={variants}
      >
        <Links />
      </motion.div>
      <ToggleButton setOpen={setOpen} />
    </motion.nav>
  );
};

export default Navbar;
