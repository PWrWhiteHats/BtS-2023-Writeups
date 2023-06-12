import "./assets/vendor/bootstrap-5.3.0-alpha3-dist/css/bootstrap.min.css";
import "./assets/vendor/bootstrap-5.3.0-alpha3-dist/js/bootstrap.bundle.min.js";
import "./assets/vendor/bootstrap-icons-1.10.5/font/bootstrap-icons.min.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";

const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(pinia);

app.mount("#app");

const tooltipTriggerList = document.querySelectorAll(
  '[data-bs-toggle="tooltip"]',
);
const tooltipList = [...tooltipTriggerList].map((tooltipTriggerEl) =>
  new bootstrap.Tooltip(tooltipTriggerEl)
);
