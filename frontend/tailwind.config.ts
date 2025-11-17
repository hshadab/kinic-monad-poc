import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Kinic official color palette (from logo)
        kinic: {
          // Light backgrounds
          light: '#ffffff',
          'light-secondary': '#f8f9fa',
          'light-tertiary': '#f1f3f5',

          // Text colors
          dark: '#1a1a1a',
          'text-primary': '#2d2d2d',
          'text-secondary': '#6b7280',

          // Kinic brand colors (from official logo)
          orange: '#F05C22',
          'orange-light': '#ff7a47',
          'orange-lighter': '#ff9770',

          yellow: '#FBAF28',
          'yellow-light': '#ffc555',
          'yellow-lighter': '#ffd780',

          cyan: '#23A8E0',
          'cyan-light': '#4db8e8',
          'cyan-lighter': '#7acbef',

          pink: '#EC1978',
          'pink-light': '#f24494',
          'pink-lighter': '#f76ab0',

          // Gray scale for lighter theme
          'gray-50': '#f9fafb',
          'gray-100': '#f3f4f6',
          'gray-200': '#e5e7eb',
          'gray-300': '#d1d5db',
          'gray-400': '#9ca3af',
          'gray-500': '#6b7280',
          'gray-600': '#4b5563',
          'gray-700': '#374151',
          'gray-800': '#1f2937',
        },
        monad: {
          primary: '#23A8E0', // Cyan from Kinic
          secondary: '#F05C22', // Orange from Kinic
        }
      },
      fontFamily: {
        sans: ['DM Sans', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-kinic': 'linear-gradient(135deg, #23A8E0 0%, #EC1978 50%, #F05C22 100%)',
        'gradient-monad': 'linear-gradient(135deg, #23A8E0 0%, #F05C22 100%)',
        'gradient-vibrant': 'linear-gradient(135deg, #FBAF28 0%, #F05C22 50%, #EC1978 100%)',
      },
    },
  },
  plugins: [],
}
export default config
