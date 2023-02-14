import { mapKeys, kebabCase } from 'lodash'
import { filename } from '@/utils/string'

import {
  mdiAlert,
  mdiAlertOctagon,
  mdiAccount,
  mdiAccountOutline,
  mdiAccountGroup,
  mdiEye,
  mdiEyeOff,
  mdiChevronUp,
  mdiContentSave,
  mdiContentCopy,
  mdiDelete,
  mdiFileDownload,
  mdiFileUpload,
  mdiFullscreen,
  mdiFullscreenExit,
  mdiHelpCircle,
  mdiHome,
  mdiKeyVariant,
  mdiLogin,
  mdiLogout,
  mdiLockOutline,
  mdiMenuDown,
  mdiPinOutline,
  mdiPinOffOutline,
  mdiPenOff,
  mdiPencil,
  mdiPaletteOutline,
  mdiRefresh,
  mdiTable,
  mdiTableRowPlusAfter,
  mdiTableRowPlusBefore,
  mdiTableOff,
  mdiTriangle,
  mdiTableEdit,
  mdiBackburger,
  mdiMenuOpen,
  mdiAlphabeticalVariant,
  mdiTranslate,
  mdiIdeogramCjkVariant,
  mdiClockOutline,
  mdiBellRemove,
  mdiBellBadgeOutline,
  mdiBellOutline,
  mdiBell,
  mdiMonitorDashboard,
  mdiViewList,
  mdiGithub,
  mdiCurrencyCny,
  mdiRss,
  mdiSend,
  mdiWeb,
  mdiAnimation,
  mdiBookOutline,
  mdiOpenInNew,
} from '@mdi/js'

const mdi = {
  mdiAccount,
  mdiAccountOutline,
  mdiAccountGroup,
  mdiEye,
  mdiEyeOff,
  mdiChevronUp,
  mdiContentSave,
  mdiContentCopy,
  mdiDelete,
  mdiFileDownload,
  mdiFileUpload,
  mdiFullscreen,
  mdiFullscreenExit,
  mdiHelpCircle,
  mdiHome,
  mdiKeyVariant,
  mdiLogin,
  mdiLogout,
  mdiLockOutline,
  mdiMenuDown,
  mdiPinOutline,
  mdiPinOffOutline,
  mdiPenOff,
  mdiPencil,
  mdiPaletteOutline,
  mdiRefresh,
  mdiTable,
  mdiTableRowPlusAfter,
  mdiTableRowPlusBefore,
  mdiTableOff,
  mdiTriangle,
  mdiTableEdit,
  mdiBackburger,
  mdiMenuOpen,
  mdiAlphabeticalVariant,
  mdiTranslate,
  mdiIdeogramCjkVariant,
  mdiClockOutline,
  mdiBellRemove,
  mdiBellBadgeOutline,
  mdiBellOutline,
  mdiBell,
  mdiMonitorDashboard,
  mdiViewList,
  mdiGithub,
  mdiCurrencyCny,
  mdiRss,
  mdiSend,
  mdiWeb,
  mdiAnimation,
  mdiBookOutline,
  mdiOpenInNew,
}

const mdIcons = mapKeys(mdi, (v, k) => kebabCase(k))
// fix vuetify#14327(https://github.com/vuetifyjs/vuetify/issues/14327)
mdIcons['warning'] = mdiAlert
mdIcons['error'] = mdiAlertOctagon

const svgIcons = Object.fromEntries(
  Object.entries(
    import.meta.glob('@/assets/icons/*.svg', {
      eager: true,
      import: 'default',
    })
  ).map(([k, v]) => [filename(k), { v }])
)

export default {
  ...svgIcons,
  ...mdIcons,
}
