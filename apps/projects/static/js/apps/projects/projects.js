async function loadProjects () {
  const grid = document.querySelector('#projects-grid')
  try {
    const r = await fetch('/api/v1/projects/')
    if (!r.ok) throw new Error()
    const projects = await r.json()
    grid.innerHTML = projects
      .map(
        (p, i) =>
          `<article class="panel project-card">${
            p.cover_image_url
              ? `<img class="project-cover" src="${p.cover_image_url}" alt="">`
              : ''
          }<div class="project-top"><span class="project-index">0${
            i + 1
          }</span><span>${
            p.is_featured ? '<span class="featured">FEATURED</span>' : ''
          } ${
            p.is_recent ? '<span class="recent">RECENT</span>' : ''
          }</span></div><h3>${p.title}</h3><p>${
            p.summary
          }</p><div class="architecture-line"><span>Architecture</span>${
            p.architecture || 'Backend system / API'
          }</div><div class="stack">${(p.tech_stack || [])
            .map(t => `<span>${t}</span>`)
            .join(
              ''
            )}</div><div class="project-actions"><a class="btn btn-primary" href="/projects/${
            p.slug
          }/">Case study →</a>${
            p.repository_url
              ? `<a class="btn btn-ghost" href="${p.repository_url}" target="_blank" rel="noreferrer">Source ↗</a>`
              : ''
          }${
            p.live_url
              ? `<a class="btn btn-ghost" href="${p.live_url}" target="_blank" rel="noreferrer">Live ↗</a>`
              : ''
          }</div></article>`
      )
      .join('')
  } catch (e) {
    grid.innerHTML =
      '<div class="panel project-card"><h3>Projects API unavailable.</h3><p>Run Django and reload.</p></div>'
  }
}
loadProjects()
