import VueI18n from 'vue-i18n'
import { castToVueI18n, createI18n } from 'vue-i18n-bridge'

import en from '@/locales/en.json'
import zh from '@/locales/zh.json'

export const install = (vue) => {
  vue.use(VueI18n, { bridge: true })

  const i18n = castToVueI18n(
    createI18n(
      {
        legacy: false,
        locale: 'en',
        messages: { zh, en },
        missingWarn: false,
        fallbackWarn: false,
      },
      VueI18n
    )
  )
  vue.use(i18n)
  return i18n
}
