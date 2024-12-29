"use client";
import { motion } from "framer-motion";
import { HeroHighlight } from "../components/hero-highlight";

export function HeroHighlightDemo() {
  return (
    <HeroHighlight >
      <motion.h1
        initial={{
          opacity: 0,
          y: 20,
        }}
        animate={{
          opacity: 1,
          y: [20, -5, 0],
        }}
        transition={{
          duration: 0.5,
          ease: [0.4, 0.0, 0.2, 1],
        }}
      >
      </motion.h1>
    </HeroHighlight>
  );
}