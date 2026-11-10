const getJSON = url =>
  fetch(url, { headers: { Accept: 'application/json' } }).then(r => {
    if (!r.ok) throw new Error()
    return r.json()
  })
const esc = (v = '') =>
  String(v).replace(
    /[&<>"']/g,
    c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[
        c
      ])
  )
function statusClass (s) {
  return `status-${s || 'degraded'}`
}
function projectCard (p, i) {
  return `<article class="panel project-card project-card-link" data-project-url="/projects/${esc(
    p.slug
  )}/"><div class="project-card-inner">${
    p.cover_image_url
      ? `<img class="project-cover" src="${esc(p.cover_image_url)}" alt="">`
      : ''
  }<div class="project-top"><span class="project-index">0${i + 1}</span><span>${
    p.is_featured ? '<span class="featured">FEATURED</span>' : ''
  } ${
    p.is_recent ? '<span class="recent">RECENT</span>' : ''
  }</span></div><h3>${esc(p.title)}</h3><p>${esc(
    p.summary
  )}</p><div class="architecture-line"><span>Architecture</span>${esc(
    p.architecture || 'Backend system / API'
  )}</div><div class="stack">${(p.tech_stack || [])
    .map(t => `<span>${esc(t)}</span>`)
    .join('')}</div><div class="project-actions">${
    p.live_url
      ? `<a class="btn btn-primary" href="${esc(
          p.live_url
        )}" target="_blank" rel="noreferrer">Live ↗</a>`
      : ''
  }${
    p.repository_url
      ? `<a class="btn btn-ghost" href="${esc(
          p.repository_url
        )}" target="_blank" rel="noreferrer">Source ↗</a>`
      : ''
  }</div></div></article>`
}
async function boot () {
  try {
    const [profile, site, projects, experience, skills, recs, recent] =
      await Promise.all([
        getJSON('/api/v1/content/profile/'),
        getJSON('/api/v1/content/site/'),
        getJSON('/api/v1/projects/?featured=true'),
        getJSON('/api/v1/content/experience/'),
        getJSON('/api/v1/content/skills/'),
        getJSON('/api/v1/content/recommendations/'),
        getJSON('/api/v1/projects/?recent=true')
      ])
    document.querySelector('#heroRole').textContent =
      profile.role_label || 'Backend Engineer'
    document.querySelector('#heroHeadline').textContent = profile.headline || ''
    document.querySelector('#heroBio').textContent = profile.short_bio || ''
    document.querySelector('#aboutShort').textContent = profile.short_bio || ''
    document.querySelector('#aboutName').textContent = profile.name || ''
    document.querySelector('#aboutRole').textContent = profile.role_label || ''
    document.querySelector('#ctaTitle').textContent =
      site.cta_title || "Let's build something."
    document.querySelector('#ctaText').textContent = site.cta_text || ''
    if (profile.email)
      document.querySelector('#ctaEmail').href = `mailto:${profile.email}`
    if (profile.avatar) {
      const img = document.querySelector('#aboutAvatar')
      img.src = profile.avatar
      img.hidden = false
    }
    document.querySelector('#featured').innerHTML =
      projects.slice(0, 3).map(projectCard).join('') ||
      '<p>No featured projects published yet.</p>'
    document.querySelector('#recent').innerHTML =
      recent.slice(0, 3).map(projectCard).join('') ||
      '<p>No recent projects published yet.</p>'
    document.querySelector('#experience').innerHTML = experience
      .slice(0, 4)
      .map(
        e =>
          `<article><time>${esc(e.start_date)} — ${
            e.is_current ? 'Present' : esc(e.end_date || '')
          }</time><h3>${esc(e.role)}${
            e.company ? ' · ' + esc(e.company) : ''
          }</h3><p>${esc(e.summary)}</p></article>`
      )
      .join('')
    const groups = {}
    skills.forEach(s => (groups[s.category] ??= []).push(s))
    document.querySelector('#skills').innerHTML = Object.entries(groups)
      .map(
        ([k, v]) =>
          `<div class="panel skill-group"><div class="skill-group-head"><h3>${esc(
            k
          )}</h3></div><p>${esc(
            v
              .map(x => x.description)
              .filter(Boolean)
              .slice(0, 1)[0] ||
              'Practical tools and engineering practices used to build dependable systems.'
          )}</p><ul>${v
            .map(x => `<li>${esc(x.name)}</li>`)
            .join('')}</ul></div>`
      )
      .join('')
    let idx = 0
    function renderRec () {
      if (!recs.length) return
      const r = recs[idx]
      document.querySelector('#recommendation').innerHTML = `${
        r.photo
          ? `<img class="testimonial-photo" src="${esc(r.photo)}" alt="${esc(
              r.name
            )}">`
          : ''
      }<blockquote>“${esc(r.message)}”</blockquote><strong>${esc(
        r.name
      )}</strong><span>${esc(r.job_title)}${
        r.company ? ' · ' + esc(r.company) : ''
      }</span>`
      document.querySelector('#recDots').innerHTML = recs
        .map((_, i) => `<span class="${i === idx ? 'active' : ''}"></span>`)
        .join('')
    }
    renderRec()
    document.querySelector('#prevRec').onclick = () => {
      idx = (idx - 1 + recs.length) % recs.length
      renderRec()
    }
    document.querySelector('#nextRec').onclick = () => {
      idx = (idx + 1) % recs.length
      renderRec()
    }
    if (recs.length > 1)
      setInterval(() => {
        idx = (idx + 1) % recs.length
        renderRec()
      }, 7000)
  } catch (e) {
    console.error(e)
  }
}
async function loadHealth () {
  const grid = document.querySelector('#health-grid'),
    time = document.querySelector('#health-time'),
    mon = document.querySelector('#project-monitoring')
  try {
    const data = await getJSON('/api/v1/dashboard/health/')
    grid.innerHTML = data.services
      .map(
        s =>
          `<article class="panel metric-card"><div class="metric-top"><span class="metric-name">${esc(
            s.name
          )}</span><span class="metric-status ${statusClass(s.status)}">● ${esc(
            s.status
          )}</span></div><div class="metric-value">${
            s.latency_ms
          }<span style="font-size:.9rem">ms</span></div><div class="metric-sub">Live probe</div></article>`
      )
      .join('')
    mon.innerHTML = (data.projects || [])
      .map(
        p =>
          `<a class="monitor-chip ${statusClass(
            p.status
          )}" href="/projects/${esc(p.slug)}/"><strong>${esc(
            p.title
          )}</strong>${esc(p.status)} · ${p.latency_ms}ms</a>`
      )
      .join('')
    time.textContent = `Updated ${new Date(
      data.generated_at
    ).toLocaleTimeString()}`
  } catch (e) {
    time.textContent = 'Telemetry unavailable'
    grid.innerHTML =
      '<div class="panel metric-card"><strong>Health API unavailable.</strong><p>Start Django and reload.</p></div>'
  }
}
boot()
loadHealth()
setInterval(loadHealth, 15000)

document.addEventListener('click', e => {
  const card = e.target.closest('.project-card-link')
  if (card && !e.target.closest('a,button')) {
    window.location.href = card.dataset.projectUrl
  }
})
