const slug = JSON.parse(document.querySelector('#projectSlug').textContent)
const escD = v =>
  String(v || '').replace(
    /[&<>"']/g,
    c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[
        c
      ])
  )
async function load () {
  const r = await fetch(`/api/v1/projects/${encodeURIComponent(slug)}/`)
  if (!r.ok) throw new Error()
  const p = await r.json()
  document.title = `${p.title} — MyPortfolio`
  document.querySelector('#projectCategory').textContent =
    p.category || 'PROJECT'
  document.querySelector('#projectTitle').textContent = p.title
  document.querySelector('#projectSummary').textContent = p.summary
  document.querySelector('#projectDescription').textContent =
    p.full_description || p.summary
  document.querySelector('#projectArchitecture').textContent =
    p.architecture ||
    'Architecture details are available in the admin project record.'
  document.querySelector('#projectAchievements').textContent =
    p.achievements || '—'
  document.querySelector('#projectChallenges').textContent = p.challenges || '—'
  document.querySelector('#projectSolutions').textContent = p.solutions || '—'
  document.querySelector('#projectStack').innerHTML = (p.tech_stack || [])
    .map(t => `<span>${escD(t)}</span>`)
    .join('')
  if (p.cover_image_url) {
    const i = document.querySelector('#projectCover')
    i.src = p.cover_image_url
    i.hidden = false
  }
  if (p.architecture_diagram_url) {
    const i = document.querySelector('#architectureDiagram')
    i.src = p.architecture_diagram_url
    i.hidden = false
  }
  document.querySelector('#projectLinks').innerHTML = `${
    p.live_url
      ? `<a class="btn btn-primary" href="${escD(
          p.live_url
        )}" target="_blank" rel="noreferrer">Live ↗</a>`
      : ''
  }${
    p.repository_url
      ? `<a class="btn btn-ghost" href="${escD(
          p.repository_url
        )}" target="_blank" rel="noreferrer">Source ↗</a>`
      : ''
  }${
    p.documentation_url
      ? `<a class="btn btn-ghost" href="${escD(
          p.documentation_url
        )}" target="_blank" rel="noreferrer">Docs ↗</a>`
      : ''
  }`
}
async function health () {
  const grid = document.querySelector('#detail-health-grid'),
    time = document.querySelector('#detail-health-time')
  try {
    const r = await fetch(
      `/api/v1/projects/${encodeURIComponent(slug)}/health/`
    )
    const h = await r.json()
    const status = h.status || 'degraded'
    let host = ''
    try {
      host = h.url ? new URL(h.url).hostname : ''
    } catch (_) {}
    grid.innerHTML = `<article class="panel metric-card"><div class="metric-top"><span class="metric-name">${escD(
      h.title || 'Live deployment'
    )}</span><span class="metric-status status-${escD(status)}">● ${escD(
      status
    )}</span></div><div class="metric-value">${
      h.latency_ms == null ? '--' : h.latency_ms
    }<span style="font-size:.9rem">${
      h.latency_ms == null ? '' : 'ms'
    }</span></div><div class="metric-sub">${
      h.http_status
        ? `HTTP ${escD(h.http_status)} · ${escD(host)}`
        : escD(h.error || 'Monitoring not configured')
    }</div></article><article class="panel metric-card"><div class="metric-top"><span class="metric-name">Endpoint</span><span class="metric-status">LIVE PROBE</span></div><div class="metric-value metric-url">${escD(
      h.url || 'Not configured'
    )}</div><div class="metric-sub">Checked ${new Date().toLocaleTimeString()}</div></article><article class="panel metric-card"><div class="metric-top"><span class="metric-name">HTTP status</span><span class="metric-status">RESPONSE</span></div><div class="metric-value">${escD(
      h.http_status ?? '--'
    )}</div><div class="metric-sub">Current response from monitored deployment</div></article><article class="panel metric-card"><div class="metric-top"><span class="metric-name">Last check</span><span class="metric-status">REAL TIME</span></div><div class="metric-value metric-time">${new Date().toLocaleTimeString()}</div><div class="metric-sub">Auto-refreshes every 15 seconds</div></article>`
    time.textContent = `Updated ${new Date().toLocaleTimeString()}`
  } catch (e) {
    grid.innerHTML =
      '<article class="panel metric-card"><strong>Telemetry unavailable.</strong><p>Unable to reach the monitoring endpoint.</p></article>'
    time.textContent = 'Telemetry unavailable'
  }
}
load().catch(() => {
  document.querySelector('#projectTitle').textContent = 'Project not found'
})
health()
setInterval(health, 15000)
