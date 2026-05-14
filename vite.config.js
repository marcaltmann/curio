import { join, resolve } from "path";
import { defineConfig } from "vite";

const INPUT_DIR = "./assets";
const OUTPUT_DIR = "./dist";

export default defineConfig({
    resolve: {
        alias: {
            "@": resolve(INPUT_DIR),
        },
    },
    base: "/static/",
    build: {
        manifest: ".vite/manifest.json",
        emptyOutDir: true,
        outDir: resolve(OUTPUT_DIR),
        rollupOptions: {
            input: {
                public: join(INPUT_DIR, "/js/public.js"),
                backoffice: join(INPUT_DIR, "/js/backoffice.js"),
            },
        },
    },
});
