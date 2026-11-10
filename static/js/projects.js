const escP = v =>
  String(v || '').replace(
    /[&<>"']/g,
    c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[
        c
      ])
  )
fetch('/api/v1/projects/')
  .then(r => r.json())
  .then(ps => {
    document.querySelector('#projects-grid').innerHTML = ps
      .map(
        (p, i) =>
          `<article class="panel project-card project-card-link" data-project-url="/projects/${escP(
            p.slug
          )}/"><div class="project-card-inner">${
            p.cover_image_url
              ? `<img class="project-cover" src="${escP(
                  p.cover_image_url
                )}" alt="">`
              : ''
          }<div class="project-top"><span class="project-index">${String(
            i + 1
          ).padStart(2, '0')}</span><span>${
            p.is_featured ? '<span class="featured">FEATURED</span>' : ''
          } ${
            p.is_recent ? '<span class="recent">RECENT</span>' : ''
          }</span></div><h3>${escP(p.title)}</h3><p>${escP(
            p.summary
          )}</p><div class="architecture-line"><span>Architecture</span>${escP(
            p.architecture || 'Backend system / API'
          )}</div><div class="tags">${(p.tech_stack || [])
            .map(t => `<span class="tag">${escP(t)}</span>`)
            .join('')}</div><div class="project-actions">${
            p.live_url
              ? `<a class="btn btn-primary" href="${escP(
                  p.live_url
                )}" target="_blank" rel="noreferrer">Live ↗</a>`
              : ''
          }${
            p.repository_url
              ? `<a class="btn btn-ghost" href="${escP(
                  p.repository_url
                )}" target="_blank" rel="noreferrer">Source ↗</a>`
              : ''
          }</div></div></article>`
      )
      .join('')
  })

document.addEventListener('click', e => {
  const card = e.target.closest('.project-card-link')
  if (card && !e.target.closest('a,button')) {
    window.location.href = card.dataset.projectUrl
  }
})
