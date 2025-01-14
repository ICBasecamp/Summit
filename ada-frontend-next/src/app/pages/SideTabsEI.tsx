"use client";
import React, { useState } from "react";
import { Sidebar, SidebarBody, SidebarLink } from "../components/side-tab";
import {
  IconArrowLeft,
  IconBrandTabler,
  IconSettings,
  IconUserBolt,
  IconBuildingStore,
  IconPercentage,
  IconBasketDollar,
  IconShoppingCart,
  IconCash,
  IconBriefcaseOff


} from "@tabler/icons-react";
import Link from "next/link";
import { motion } from "framer-motion";
import Image from "next/image";
import { cn } from "../../../lib/utils";

export function SidebarDemo({ children }: { children: React.ReactNode }) {
  const links = [
    {
      label: "Retail Sales",
      href: `/economic-indicators/retail-sales`,
      icon: (
        <IconBuildingStore className="text-neutral-100 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "FED Rate",
      href: `/economic-indicators/fed-rate`,
      icon: (
        <IconPercentage className="text-neutral-100 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "Durable Goods",
      href: `/economic-indicators/durable-goods`,
      icon: (
        <IconBasketDollar className="text-neutral-100 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "CPI",
      href: `/economic-indicators/cpi`,
      icon: (
        <IconShoppingCart className="text-neutral-100 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "Nonfarm Payroll",
      href: `/economic-indicators/nonfarm-payroll`,
      icon: (
        <IconCash className="text-neutral-100 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "Unemployment Rate",
      href: `/economic-indicators/unemployment-rate`,
      icon: (
        <IconBriefcaseOff className="text-neutral-100 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
  ];

  const [open, setOpen] = useState(false);
  return (
    <div
      className={cn(
        "flex flex-col md:flex-row bg-neutral-900 dark:bg-neutral-800 w-full flex-1 border border-neutral-700 dark:border-neutral-700 overflow-hidden",
        "h-full" // Adjusted height for your use case
      )}
    >
      <Sidebar open={open} setOpen={setOpen}>
        <SidebarBody className="justify-between gap-10">
          <div className="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <div className="mt-8 flex flex-col gap-2">
              {links.map((link, idx) => (
                <SidebarLink key={idx} link={link} />
              ))}
            </div>
          </div>
        </SidebarBody>
      </Sidebar>
      {children}
    </div>
  );
}