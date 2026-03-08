import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        saffron: {
          DEFAULT: "#E8610A",
          light: "#FFF3E8",
          dark: "#B84D08",
        },
        indigo: {
          DEFAULT: "#1A1560",
          light: "#EEF2FF",
          dark: "#0F0D3A",
        },
        forest: {
          DEFAULT: "#006B47",
          light: "#ECFDF5",
        },
        surface: "#FAFAF8",
        "surface-2": "#F3F4F6",
        "text-primary": "#1C1C1C",
        "text-dim": "#6B7280",
        border: "#E5E7EB",
      },
      fontFamily: {
        sans: ["Noto Sans", "system-ui", "sans-serif"],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
