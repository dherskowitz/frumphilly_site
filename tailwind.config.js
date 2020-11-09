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
            },
            height: {
                25: "25vh",
                40: "40vh",
                50: "50vh",
                60: "60vh",
                100: "100vh",
            },
            inset: {
                "avoid-header": "4rem",
                "-1": "-1rem",
                "-2": "-2rem",
                "-4": "-3.5rem",
            },
            margin: {
                "18": "4.5rem",
            },
            zIndex: {
                "-1": "-1",
            },
            fontSize: {
                "4.5xl": "2.5rem",
            },
            height: {
                "cust-screen": "calc(100vh - 8rem)",
                "half-screen": "60vh",
                "vh-full": "100vh",
            },
        },
        container: {
            center: true,
            padding: "1rem",
        },
    },
    textShadow: {
        default: "2px 2px 3px #000",
    },
    variants: {
        textColor: ["group-hover", "hover"],
        textShadow: ["responsive"],
        scale: ["responsive", "hover", "group-hover"],
        letterSpacing: ["group-hover"],
        backgroundSize: ["responsive", "hover", "group-hover"],
        backgroundColor: ['responsive', 'hover', 'even'],
    },
    plugins: [
        plugin(function({
            addUtilities
        }) {
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
