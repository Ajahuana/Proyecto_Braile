import fs from "fs";
import path from "path";

const filePath = path.join(process.cwd(), "data", "libros.json");

function leerLibros() {
    const json = fs.readFileSync(filePath, "utf8");
    return JSON.parse(json);
}

function escribirLibros(libros) {
    fs.writeFileSync(filePath, JSON.stringify(libros, null, 2));
}

export default defineEventHandler(async (event) => {
    const method = event.req.method;

    if (method === "GET") {
        return leerLibros();
    }

    if (method === "POST") {
        const body = await readBody(event);
        const libros = leerLibros();
        const nuevoLibro = { id: Date.now(), ...body };
        libros.push(nuevoLibro);
        escribirLibros(libros);
        return { success: true, libro: nuevoLibro };
    }

    if (method === "PUT") {
        const body = await readBody(event);
        let libros = leerLibros();
        libros = libros.map((l) => (l.id === body.id ? { ...l, ...body } : l));
        escribirLibros(libros);
        return { success: true };
    }

    if (method === "DELETE") {
        const body = await readBody(event); // { id }
        let libros = leerLibros();
        libros = libros.filter((l) => l.id !== body.id);
        escribirLibros(libros);
        return { success: true };
    }

    return { error: "Método no soportado" };
});
