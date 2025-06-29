// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  runtimeConfig: {
    mongodbUri: process.env.MONGODB_URI,
  },
  public: {
    data: "~/data",
  },
  app: {
    head: {
      charset: "utf-8",
      viewport:
        "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0",
    },
  },
  build: {
    analyze: true,
  },
  nitro: {
    routeRules: {
      "/api/**": { cors: true },
    },
  },
  modules: [
    "nuxt-auth-utils",
    "@nuxtjs/google-fonts",
    "@nuxt/image",
    "@nuxtjs/tailwindcss",
  ],
  auth: {
    baseURL: process.env.BASE_URL || "http://localhost:3001",
    provider: {
      type: "local",
      endpoints: {
        signIn: { path: "/api/auth/login-request", method: "post" },
        signOut: { path: "/api/auth/logout", method: "post" },
        session: { path: "/api/auth/verify", method: "get" },
      },
    },
  },
  googleFonts: {
    download: false,
    families: {
      Roboto: [400, 700],
      "Roboto Slab": [800],
    },
    display: "swap",
  },
  vue: {
    compilerOptions: {
      isCustomElement: (tag) => tag.includes("swiper"),
    },
  },
  image: {
    provider: "netlify",
    format: ["webp"],
    quality: 20,
  },
  compatibilityDate: "2024-08-10",
});
