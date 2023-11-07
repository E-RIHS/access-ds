import { entry as extendedStringControlRenderer} from './ExtendedStringControlRenderer.vue'
import { entry as extendedEnumControlRenderer} from './ExtendedEnumControlRenderer.vue'
import { entry as extendedEnumApiControlRenderer} from './ExtendedEnumApiControlRenderer.vue'

const customRenderers = [
    extendedStringControlRenderer,
    extendedEnumControlRenderer,
    extendedEnumApiControlRenderer
]

export default customRenderers
