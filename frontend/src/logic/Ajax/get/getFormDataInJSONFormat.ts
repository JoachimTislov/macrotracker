export function getFormDataInJSONFormat(identifier: string) {
  const form = document.getElementById(identifier) as HTMLFormElement
  const formData = new FormData(form)

  const jsonData: { [key: string]: {} } = {}
  for (const [key, value] of formData.entries()) {
    jsonData[key] = value
  }

  return JSON.stringify(jsonData)
}
