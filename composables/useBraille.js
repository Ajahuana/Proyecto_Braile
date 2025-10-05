// /composables/useBraille.js
import { computed, ref } from "vue";

export function useBraille(textoInicial = "") {
    const libro = ref(textoInicial);

    const diccionarioBraille = {
        a: "⠁",
        b: "⠃",
        c: "⠉",
        d: "⠙",
        e: "⠑",
        f: "⠋",
        g: "⠛",
        h: "⠓",
        i: "⠊",
        j: "⠚",
        k: "⠅",
        l: "⠇",
        m: "⠍",
        n: "⠝",
        ñ: "⠻",
        o: "⠕",
        p: "⠏",
        q: "⠟",
        r: "⠗",
        s: "⠎",
        t: "⠞",
        u: "⠥",
        v: "⠧",
        w: "⠺",
        x: "⠭",
        y: "⠽",
        z: "⠵",
        á: "⠷",
        é: "⠮",
        í: "⠌",
        ó: "⠬",
        ú: "⠾",
        ü: "⠳",
        " ": " ", // espacio como “cero” Braille
        1: "⠁",
        2: "⠃",
        3: "⠉",
        4: "⠙",
        5: "⠑",
        6: "⠋",
        7: "⠛",
        8: "⠓",
        9: "⠊",
        0: "⠚",
    };

    const simbolos_braille = {
        ".": "⠄",
        ",": "⠂",
        ";": "⠆",
        ":": "⠒",
        "?": "⠢",
        "¿": "⠢",
        "!": "⠖",
        "¡": "⠖",
        '"': "⠦",
        "“": "⠦",
        "”": "⠴",
        "«": "⠦",
        "»": "⠴",
        "<": "⠦",
        ">": "⠴",
        "'": "⠄",
        "‘": "⠦",
        "’": "⠦",
        "(": "⠣",
        ")": "⠜",
        _: "⠤",
        "-": "⠤",
        "/": "⠌",
        "{": "⠨",
        "#": "⠼",
        "+": "⠖",
        "=": "⠶",
        "%": "⠨⠴",
        "@": "⠐",
    };

    const monedas_braille = {
        "€": ["⠸", "⠑"],
        $: ["⠸", "⠎"],
        Bs: ["⠸", "⠃", "⠎"],
        "¢": ["⠸", "⠉"],
        R$: ["⠸", "⠗"],
        DM: ["⠸", "⠍"],
        "¥": ["⠸", "⠽"],
        "₿": ["⠸", "⠃"],
    };

    const mayuscula = "⠨";
    const numero = "⠼";
    const longitudLinea = 29; // longitud máxima de línea

    const traducido = computed(() => {
        let resultado = "";
        let enNumero = false;

        // Traducción carácter por carácter
        let traducidoRaw = "";
        const palabras_entrada = libro.value.split(/(\s+)/); // incluye espacios, tabs, saltos de línea como elementos

        for (let palabra of palabras_entrada) {
            if (palabra.trim() === "") {
                traducidoRaw += palabra; // espacios, tabs, saltos
                continue;
            }

            // Verificar si es número puro
            if (/^\d+$/.test(palabra)) {
                for (let digito of palabra) {
                    traducidoRaw +=
                        numero + (diccionarioBraille[digito] || digito);
                }
                continue;
            }

            // Verificar si es palabra totalmente en mayúsculas (mínimo 2 letras)
            if (
                palabra.length > 1 &&
                palabra === palabra.toUpperCase() &&
                /[A-ZÁÉÍÓÚÜÑ]/.test(palabra)
            ) {
                traducidoRaw += mayuscula + mayuscula;
                for (let char of palabra.toLowerCase()) {
                    traducidoRaw +=
                        diccionarioBraille[char] ||
                        simbolos_braille[char] ||
                        char;
                }
                continue;
            }

            // Mixto o minúsculas normales
            let enNumero = false;
            for (let i = 0; i < palabra.length; i++) {
                const char = palabra[i];

                // Monedas
                let moneda = null;
                for (const key in monedas_braille) {
                    if (palabra.startsWith(key, i)) {
                        moneda = monedas_braille[key].join("");
                        i += key.length - 1;
                        break;
                    }
                }
                if (moneda) {
                    traducidoRaw += moneda;
                    enNumero = false;
                    continue;
                }

                // Números individuales
                if (/[0-9]/.test(char)) {
                    traducidoRaw += numero + (diccionarioBraille[char] || char);
                    enNumero = true;
                    continue;
                } else {
                    enNumero = false;
                }

                // Mayúscula individual
                if (
                    char.toUpperCase() === char &&
                    char.toLowerCase() !== char
                ) {
                    traducidoRaw +=
                        mayuscula +
                        (diccionarioBraille[char.toLowerCase()] || char);
                    continue;
                }

                // Símbolo
                if (simbolos_braille[char]) {
                    traducidoRaw += simbolos_braille[char];
                    continue;
                }

                // Letra minúscula
                traducidoRaw += diccionarioBraille[char] || char;
            }
        }

        // Formatear líneas de longitud fija sin cortar palabras
        const palabras = traducidoRaw.split(" ");
        let linea = "";
        for (let i = 0; i < palabras.length; i++) {
            let palabra = palabras[i];
            if (linea.length + palabra.length > longitudLinea) {
                linea = linea.padEnd(longitudLinea, " ");
                resultado += linea + "\n";
                linea = palabra;
            } else {
                if (linea.length > 0) linea += " "; // espacio entre palabras
                linea += palabra;
            }
        }

        // Última línea
        if (linea.length > 0) {
            linea = linea.padEnd(longitudLinea, " ");
            resultado += linea;
        }

        return resultado;
    });

    return { libro, traducido };
}
