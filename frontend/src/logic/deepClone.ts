export default function deepClone<T>(element: T) {
  return JSON.parse(JSON.stringify(element))
}
