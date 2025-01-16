"use client";

import { useState } from "react";
import Link from 'next/link';
import { motion } from "framer-motion";
import { cn } from "../../../lib/utils";

import { useRouter, usePathname } from 'next/navigation';
import { Open_Sans } from 'next/font/google';

const openSans = Open_Sans({ subsets: ['latin'] })

type Tab = {
  title: string;
  value: string;
  content?: string | React.ReactNode | any;
};

export const Tabs = ({
  tabs: propTabs,
  containerClassName,
  activeTabClassName,
  tabClassName,
  contentClassName,
}: {
  tabs: Tab[];
  containerClassName?: string;
  activeTabClassName?: string;
  tabClassName?: string;
  contentClassName?: string;
}) => {
  const [tabs, setTabs] = useState<Tab[]>(propTabs);

  const pathname = usePathname();

  const currentTab = pathname.split('/')[1];

  const active = tabs.find((tab) => tab.value.split("/")[0] === currentTab) || tabs[0];

  const moveSelectedTabToTop = (idx: number) => {
    const newTabs = [...tabs];
    const [selectedTab] = newTabs.splice(idx, 1);
    newTabs.unshift(selectedTab);
    setTabs(newTabs);
  };

  const [hovering, setHovering] = useState(false);

  return (
    <>
      <div
        className={cn(
          "flex flex-row items-center justify-start [perspective:1000px] relative overflow-auto sm:overflow-visible no-visible-scrollbar max-w-full w-full",
          containerClassName
        )}
      >
        {propTabs.map((tab, idx) => (
          <Link href={`/${tab.value}`} key={tab.title}>
            <button
              onClick={() => {
                moveSelectedTabToTop(idx);
              }}
              onMouseEnter={() => setHovering(true)}
              onMouseLeave={() => setHovering(false)}
              className={cn("relative px-6 py-3 rounded-full", tabClassName)}
              style={{
                transformStyle: "preserve-3d",
              }}
            >
              {active.value === tab.value && (
                <motion.div
                  layoutId="clickedbutton"
                  transition={{ type: "spring", bounce: 0.3, duration: 0.6 }}
                  className={cn(
                    "absolute inset-0 bg-neutral-800 dark:bg-zinc-900 rounded-full ",
                    activeTabClassName
                  )}
                />
              )}

              <span className={cn("relative block text-white dark:text-white")}>
                {tab.title}
              </span>
            </button>
          </Link>
        ))}
      </div>
    </>
  );
};
