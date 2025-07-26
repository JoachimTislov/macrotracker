import type { ComponentOptionsBase, ComponentPublicInstance } from 'vue'

type vueElement =
  | Element
  | ComponentPublicInstance<
      {},
      {},
      {},
      {},
      {},
      {},
      {},
      {},
      false,
      ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}>,
      {},
      {}
    >
  | null

export function setElementReference(element: vueElement, divRef: HTMLElement | null) {
  divRef = element as HTMLElement
  return divRef
}
