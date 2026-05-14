import "vite/modulepreload-polyfill";

import Alpine from "alpinejs";

import "@/css/backoffice.css";

// Initialize Alpine.js
window.Alpine = Alpine;
Alpine.start();
