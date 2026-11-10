document.querySelector('#trigger').onclick = async () => {
  const id = document.querySelector('#projectId').value
  const r = await fetch(`/api/v1/projects/${id}/sandbox-trigger/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
  document.querySelector('#labOutput').textContent = JSON.stringify(
    await r.json(),
    null,
    2
  )
}
