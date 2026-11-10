const escA = v =>
  String(v || '').replace(
    /[&<>"']/g,
    c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[
        c
      ])
  )
const iconGithub =
  '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .7A11.3 11.3 0 0 0 8.43 22.8c.56.1.77-.24.77-.54v-2.1c-3.14.68-3.8-1.33-3.8-1.33-.51-1.3-1.25-1.65-1.25-1.65-1.02-.7.08-.68.08-.68 1.13.08 1.73 1.16 1.73 1.16 1 .1 1.57.99 1.57.99.9 1.56 2.35 1.11 2.93.85.1-.67.35-1.11.64-1.37-2.51-.29-5.15-1.26-5.15-5.6 0-1.24.44-2.25 1.16-3.04-.12-.29-.5-1.45.11-3.02 0 0 .95-.3 3.11 1.16a10.8 10.8 0 0 1 5.66 0c2.16-1.46 3.1-1.16 3.1-1.16.61 1.57.23 2.73.12 3.02.72.79 1.16 1.8 1.16 3.04 0 4.35-2.65 5.3-5.17 5.59.36.31.68.92.68 1.85v2.74c0 .3.2.65.78.54A11.3 11.3 0 0 0 12 .7Z"/></svg>'
const iconLinkedin =
  '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M5.1 3.7A2.1 2.1 0 1 1 .9 3.7a2.1 2.1 0 0 1 4.2 0ZM1.1 8.1h4v12.8h-4V8.1Zm6.5 0h3.8v1.75h.05c.53-1 1.83-2.05 3.76-2.05 4.02 0 4.76 2.65 4.76 6.1v7h-4v-6.2c0-1.48-.03-3.38-2.06-3.38-2.07 0-2.38 1.61-2.38 3.27v6.31h-3.93V8.1Z"/></svg>'
fetch('/api/v1/content/about/')
  .then(r => r.json())
  .then(d => {
    const p = d.profile || {}
    document.querySelector('#name').textContent = p.name || 'About'
    document.querySelector('#role').textContent = p.role_label || ''
    document.querySelector('#bio').textContent = p.full_bio || p.short_bio || ''
    document.querySelector('#aboutLocation').textContent = p.location || ''
    const email = document.querySelector('#aboutEmail')
    email.textContent = p.email || ''
    email.href = p.email ? `mailto:${p.email}` : ''
    if (p.avatar) {
      const i = document.querySelector('#aboutAvatar')
      i.src = p.avatar
      i.hidden = false
    }
    document.querySelector('#aboutSocial').innerHTML = [
      p.github_url
        ? `<a class="btn btn-ghost social-btn" href="${escA(
            p.github_url
          )}" target="_blank" rel="noreferrer">${iconGithub}<span>GitHub</span></a>`
        : '',
      p.linkedin_url
        ? `<a class="btn btn-ghost social-btn" href="${escA(
            p.linkedin_url
          )}" target="_blank" rel="noreferrer">${iconLinkedin}<span>LinkedIn</span></a>`
        : ''
    ]
      .filter(Boolean)
      .join('')
    document.querySelector('#aboutExperience').innerHTML = (d.experience || [])
      .map(
        e =>
          `<article><time>${escA(e.start_date)} — ${
            e.is_current ? 'Present' : escA(e.end_date)
          }</time><h3>${escA(e.role)}${
            e.company ? ' · ' + escA(e.company) : ''
          }</h3><p>${escA(e.summary)}</p></article>`
      )
      .join('')
    const g = {}
    ;(d.skills || []).forEach(s => (g[s.category] ??= []).push(s))
    document.querySelector('#aboutSkills').innerHTML = Object.entries(g)
      .map(
        ([k, v]) =>
          `<div class="panel skill-group"><div class="skill-group-head"><h3>${escA(
            k
          )}</h3></div><ul>${v
            .map(x => `<li>${escA(x.name)}</li>`)
            .join('')}</ul></div>`
      )
      .join('')
  })
