import Vue from 'vue'
import Vuetify from 'vuetify/lib'
//import icons from './icons'
//import { useDark } from '@vueuse/core'
import en from 'vuetify/lib/locale/en'
import zh from 'vuetify/lib/locale/zh-Hans'

import colors from 'vuetify/lib/util/colors'

const theme = {
    primary: colors.purple,
    secondary: colors.grey.darken1,
    accent: colors.shades.black,
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107',
}

Vue.use(Vuetify)

export default new Vuetify({
    lang: {
        locales: { zh, en },
        current: 'en',
    },
    // theme: {
    //   dark: useDark().value,
    //   themes: {
    //     light: theme,
    //     dark: theme,
    //   },
    //   options: {
    //     themeCache: {
    //       // https://vuetifyjs.com/features/theme/#section-30ad30e330c330b730e5
    //       get: (key) => {
    //         return localStorage.getItem(`parsed-theme-${key.primary.base}`)
    //       },
    //       set: (key, value) => {
    //         localStorage.setItem(`parsed-theme-${key.primary.base}`, value)
    //       },
    //     },
    //     customProperties: true,
    //   },
    // },
    // icons: {
    //   iconfont: 'mdiSvg',
    //   values: {
    //     ...icons,
    //   },
    // },
    // breakpoint: {
    //   thresholds: {
    //     xs: 600,
    //     sm: 960,
    //     md: 1280,
    //     lg: 1920,
    //   },
    //   mobileBreakpoint: 'sm',
    //   scrollBarWidth: 0,
    // },
})
