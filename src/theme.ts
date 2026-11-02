import { Easing } from "remotion";

export const theme = {
  colors: {
    bg: "#0A0D14",
    bgAlt: "#0F172A",
    primary: "#EAB308", // THE hero color (Gold/Yellow) - max one element per frame
    accent: "#38BDF8",  // Cyan
    danger: "#EF4444",  // Alert red
    text: "#F8FAFC",
    textDim: "#94A3B8",
    glow: "rgba(234, 179, 8, 0.35)",
  },
  fonts: {
    display: "Segoe UI, Arial, sans-serif",
    body: "Segoe UI, Arial, sans-serif",
  },
  ease: {
    out: Easing.bezier(0.16, 1, 0.3, 1), // easeOutExpo — entrances
    inOut: Easing.bezier(0.83, 0, 0.17, 1), // easeInOutQuint — moves, Ken Burns
    in: Easing.bezier(0.7, 0, 0.84, 0), // exits only
  },
  spring: {
    snappy: { damping: 14, stiffness: 160, mass: 0.6 }, // UI pops, words
    smooth: { damping: 20, stiffness: 90, mass: 1 },    // big elements
    bouncy: { damping: 11, stiffness: 170, mass: 0.7 },  // playful accents
  },
} as const;
