const form = document.querySelector('#sandbox-form')
const projectSelect = document.querySelector('#project-select')
const methodSelect = document.querySelector('#method-select')
const payloadInput = document.querySelector('#payload-input')
const output = document.querySelector('#result-output')
const error = document.querySelector('#sandbox-error')
const resultTime = document.querySelector('#result-time')

async function init () {
  try {
    const response = await fetch('/api/v1/projects/')
    if (!response.ok) throw new Error('Could not load projects.')
    const projects = await response.json()
    projectSelect.innerHTML = projects
      .map(p => `<option value="${p.id}">${p.title}</option>`)
      .join('')
  } catch (err) {
    error.textContent = err.message
  }
}

form.addEventListener('submit', async event => {
  event.preventDefault()
  error.textContent = ''
  output.className = 'trace-empty'
  output.textContent = 'Processing request…'
  resultTime.textContent = 'RUNNING'

  let payload
  try {
    payload = JSON.parse(payloadInput.value)
  } catch {
    error.textContent = 'Payload is not valid JSON.'
    resultTime.textContent = 'INVALID'
    return
  }

  try {
    const response = await fetch(
      `/api/v1/projects/${projectSelect.value}/sandbox-trigger/`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ method: methodSelect.value, payload })
      }
    )
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || 'Sandbox request failed.')

    output.className = 'trace'
    output.innerHTML = `
      ${data.steps
        .map(
          item => `
        <div class="trace-step">
          <span class="step">${item.step}</span>
          <span class="status">${item.status}</span>
          <span>${item.detail}</span>
        </div>
      `
        )
        .join('')}
      <div class="response-box">
        <pre>${JSON.stringify(data.response, null, 2)}</pre>
      </div>
    `
    resultTime.textContent = `${data.duration_ms}ms`
  } catch (err) {
    error.textContent = err.message
    resultTime.textContent = 'ERROR'
    output.className = 'trace-empty'
    output.textContent = 'Request failed.'
  }
})

init()
