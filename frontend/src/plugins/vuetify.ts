import { createVuetify, ThemeDefinition } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

// Styles
import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";

const customTheme: ThemeDefinition = {
  dark: false,
  colors: {
    background: "#5f9ea0",
    primary: "#F0F0E0",
    secondary: "#263238",
    error: "#f44336",
    info: "#8bc34a",
    success: "#4caf50",
    warning: "#ff9800",
    setting: "#607d8b",
  },
};

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: "customTheme",
    themes: {
      customTheme,
    },
  },
});

export default vuetify;
