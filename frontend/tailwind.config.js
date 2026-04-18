/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Onest', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        display: ['Unbounded', 'sans-serif'],
      },
      colors: {
        ink: {
          DEFAULT: '#0D0F14',
          50: '#F5F6F8',
          100: '#EAEDF2',
          200: '#CDD3DF',
          300: '#9FAAB9',
          400: '#6B7A91',
          500: '#4A5568',
          600: '#2D3748',
          700: '#1A2232',
          800: '#111827',
          900: '#0D0F14',
        },
        accent: {
          DEFAULT: '#5B6EF5',
          50: '#EEF0FE',
          100: '#DDE1FD',
          200: '#BAC3FB',
          300: '#8896F9',
          400: '#5B6EF5',
          500: '#3B4FE8',
          600: '#2A3CD0',
          700: '#1E2CA8',
          800: '#141D75',
          900: '#0A1042',
        },
        jade: {
          DEFAULT: '#10B981',
          50: '#ECFDF5',
          100: '#D1FAE5',
          400: '#34D399',
          500: '#10B981',
          600: '#059669',
        },
        amber: {
          DEFAULT: '#F59E0B',
          50: '#FFFBEB',
          100: '#FEF3C7',
          400: '#FBBF24',
          500: '#F59E0B',
          600: '#D97706',
        },
        rose: {
          DEFAULT: '#F43F5E',
          50: '#FFF1F2',
          100: '#FFE4E6',
          400: '#FB7185',
          500: '#F43F5E',
          600: '#E11D48',
        },
        surface: {
          DEFAULT: '#FFFFFF',
          50: '#FAFAFA',
          100: '#F4F6F9',
          200: '#EAECF0',
        }
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
        '3xl': '24px',
      },
      boxShadow: {
        'soft': '0 1px 3px rgba(13,15,20,0.06), 0 4px 16px rgba(13,15,20,0.06)',
        'card': '0 2px 8px rgba(13,15,20,0.08), 0 8px 32px rgba(13,15,20,0.06)',
        'lift': '0 8px 24px rgba(13,15,20,0.12), 0 2px 8px rgba(13,15,20,0.08)',
        'glow': '0 0 0 3px rgba(91,110,245,0.15)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease forwards',
        'slide-up': 'slideUp 0.4s cubic-bezier(0.16,1,0.3,1) forwards',
        'slide-in-right': 'slideInRight 0.4s cubic-bezier(0.16,1,0.3,1) forwards',
        'scale-in': 'scaleIn 0.25s cubic-bezier(0.16,1,0.3,1) forwards',
        'pulse-soft': 'pulseSoft 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: { from: { opacity: '0' }, to: { opacity: '1' } },
        slideUp: { from: { opacity: '0', transform: 'translateY(12px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        slideInRight: { from: { opacity: '0', transform: 'translateX(20px)' }, to: { opacity: '1', transform: 'translateX(0)' } },
        scaleIn: { from: { opacity: '0', transform: 'scale(0.95)' }, to: { opacity: '1', transform: 'scale(1)' } },
        pulseSoft: { '0%,100%': { opacity: '1' }, '50%': { opacity: '0.6' } },
      }
    }
  },
  plugins: []
}
