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
        'avoid-header': '4rem'
      }
    },
    textShadow: {
      'default': '2px 2px 3px #000',
    }
  },
  variants: {},
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
