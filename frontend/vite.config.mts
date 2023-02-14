import path from 'path'
import vue2 from '@vitejs/plugin-vue2'
import legacy from '@vitejs/plugin-legacy'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { createSvgPlugin } from '@kingyue/vite-plugin-vue2-svg'
import { splitVendorChunkPlugin } from 'vite'
import Pages from 'vite-plugin-pages'
//import Layouts from 'vite-plugin-vue-layouts'
import VueI18n from '@intlify/unplugin-vue-i18n/vite'
import browserslistToEsbuild from 'browserslist-to-esbuild'
import SupportedBrowsers from 'vite-plugin-browserslist-useragent'

// https://vitejs.dev/config/
export default {
    build: { target: browserslistToEsbuild() },
    server: {
        port: 8001,
    },
    plugins: [
        vue2(),
        Pages(),
        legacy({
            // Plugin does not use browserslistrc https://github.com/vitejs/vite/issues/2476
            modernPolyfills: true,
            renderLegacyChunks: false,
        }),
        Components({
            resolvers: [
                {
                    type: 'component',
                    resolve: (name) => {
                        const blackList = []
                        if (name.match(/^V[A-Z]/) && !blackList.includes(name))
                            return { name, from: 'vuetify/lib' }
                    },
                },
            ],
            dirs: [],
            dts: false,
            types: [],
        }),
        AutoImport({
            imports: [
                'vue',
                {
                    'vue-i18n-bridge': ['useI18n'],
                    'vue-router/composables': [
                        'useRoute',
                        'useRouter',
                        'useLink',
                        'onBeforeRouteUpdate',
                        'onBeforeRouteLeave',
                    ],
                    'axios': [
                        ['default', 'axios'],
                    ],
                },
            ],
            dts: 'src/auto-imports.d.ts',
            dirs: ['src/components'],
            vueTemplate: false,
        }),
        createSvgPlugin(),
        splitVendorChunkPlugin(),
        VueI18n({
            runtimeOnly: false,
            compositionOnly: true,
            fullInstall: false,
            include: [path.resolve(__dirname, 'src/locales/**')],
        }),
        SupportedBrowsers(),
    ],
    css: {
        devSourcemap: true,
        // https://vitejs.dev/config/#css-preprocessoroptions
        preprocessorOptions: {
            sass: {
                additionalData: [
                    // vuetify variable overrides
                    '@import "@/assets/styles/vuetify-variables.scss"',
                    '',
                ].join('\n'),
            },
        },
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, 'src'),
            'vue-echarts': 'vue-echarts/dist/index.esm.min.js',
            'vue-i18n-bridge':
                'vue-i18n-bridge/dist/vue-i18n-bridge.runtime.esm-bundler.js',
        },
    },
}
