import { motion } from "framer-motion";
import { navLinks } from "../constants";

const variants = {
  open: {
    transition: {
      staggerChildren: 0.1,
    },
  },
  closed: {
    transition: {
      staggerChildren: 0.05,
      staggerDirection: -1,
    },
  },
};

const itemVariants = {
  open: {
    y: 0,
    opacity: 1,
  },
  closed: {
    y: 50,
    opacity: 0,
  },
};

const Links = () => {
  return (
    <motion.div
      className="links absolute, w-[100%] h-[100%] flex flex-col justify-center items-center"
      variants={variants}
    >
      {navLinks.map((menuItem) => (
        <motion.a
          className="text-white mb-7 font-inter text-4xl"
          href={`#${menuItem.id}`}
          key={menuItem.id}
          variants={itemVariants}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
        >
          {menuItem.title}
        </motion.a>
      ))}
    </motion.div>
  );
};

export default Links;
