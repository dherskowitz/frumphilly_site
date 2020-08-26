const plugin = require('tailwindcss/plugin')

module.exports = {
  purge: [],
  theme: {
    extend: {
      colors: {
        bgGrey: 'rgba(210, 215, 211, 1)',
      },
      height: {
        25: '25vh',
        40: '40vh',
        50: '50vh',
        60: '60vh',
        100: '100vh'
      },
      inset: {
        'avoid-header': '4rem',
        '-2': '-2rem',
        '-4': '-3.5rem'
      }
    },
    textShadow: {
      'default': '2px 2px 3px #000',
    },
    zIndex: {
      '-1': '-1',
    }
  },
  variants: {
    textColor: ['group-hover'],
  },
  plugins: [
    plugin(function ({
      addUtilities
    }) {
      const addShadows = {
        '.text-shadow': {
          'text-shadow': '2px 2px 3px #000',
        },
      }
      addUtilities(addShadows)
    })
  ],
}
