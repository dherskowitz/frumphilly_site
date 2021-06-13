const plugin = require("tailwindcss/plugin");

module.exports = {
    purge: [],
    theme: {
        extend: {
            colors: {
                bgGrey: "rgba(210, 215, 211, 1)",
                silver: "rgba(191, 191, 191, 1)",
                "transparent-red": "rgba(211, 67, 62, 0.1)",
                google: "#ea4335",
                facebook: "#3b5998",
                fpPurple: "#684072",
                fpRed: "#d8423d"
            },
            height: {
                25: "25vh",
                40: "40vh",
                50: "50vh",
                60: "60vh",
                100: "100vh",
                // "cust-screen": "calc(100vh - 15.25rem)",
                "half-screen": "60vh",
                "vh-full": "100vh",
            },
            margin: {
                18: "4.5rem",
            },
            zIndex: {
                "-1": "-1",
            },
            fontSize: {
                "4.5xl": "2.5rem",
            },
        },
        container: {
            center: true,
            padding: "1rem",
        },
    },
    variants: {
        textShadow: ["responsive"],
        extend: {
            opacity: ['disabled'],
            pointerEvents: ['disabled'],
            stroke: ['hover'],
            textColor: ["group-hover", "hover"],
            translate: ["hover", "group-hover"],
            scale: ["responsive", "hover", "group-hover"],
            letterSpacing: ["group-hover"],
            backgroundSize: ["responsive", "hover", "group-hover"],
            backgroundColor: ["responsive", "hover", "even"],
        },
    },
    textShadow: {
        default: "2px 2px 3px #000",
    },
    plugins: [
        plugin(function ({ addUtilities }) {
            const addShadows = {
                ".text-shadow": {
                    "text-shadow": "2px 2px 3px #000",
                },
                ".text-shadow-0": {
                    "text-shadow": "none",
                },
            };
            addUtilities(addShadows, {
                variants: ["responsive"],
            });
        }),
    ],
};
