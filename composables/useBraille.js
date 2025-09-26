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
        "@": "⠈⠁",
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
        for (let i = 0; i < libro.value.length; i++) {
            let char = libro.value[i];

            // Detectar monedas (ej: Bs, R$, DM)
            let moneda = null;
            for (const key in monedas_braille) {
                if (libro.value.startsWith(key, i)) {
                    moneda = monedas_braille[key].join("");
                    i += key.length - 1; // avanzar índice
                    break;
                }
            }
            if (moneda) {
                traducidoRaw += moneda;
                enNumero = false;
                continue;
            }

            // Mayúscula
            if (char.toUpperCase() === char && char.toLowerCase() !== char) {
                traducidoRaw +=
                    mayuscula +
                    (diccionarioBraille[char.toLowerCase()] || char);
                enNumero = false;
                continue;
            }

            // Número
            if (/[0-9]/.test(char)) {
                if (!enNumero) {
                    traducidoRaw += numero;
                    enNumero = true;
                }
                traducidoRaw += diccionarioBraille[char] || char;
                continue;
            } else {
                enNumero = false;
            }

            // Símbolos
            if (simbolos_braille[char]) {
                traducidoRaw += simbolos_braille[char];
            } else {
                // Letras y otros
                traducidoRaw += diccionarioBraille[char.toLowerCase()] || char;
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
