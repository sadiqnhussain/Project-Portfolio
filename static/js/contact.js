const iconGithub =
  '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .7A11.3 11.3 0 0 0 8.43 22.8c.56.1.77-.24.77-.54v-2.1c-3.14.68-3.8-1.33-3.8-1.33-.51-1.3-1.25-1.65-1.25-1.65-1.02-.7.08-.68.08-.68 1.13.08 1.73 1.16 1.73 1.16 1 .1 1.57.99 1.57.99.9 1.56 2.35 1.11 2.93.85.1-.67.35-1.11.64-1.37-2.51-.29-5.15-1.26-5.15-5.6 0-1.24.44-2.25 1.16-3.04-.12-.29-.5-1.45.11-3.02 0 0 .95-.3 3.11 1.16a10.8 10.8 0 0 1 5.66 0c2.16-1.46 3.1-1.16 3.1-1.16.61 1.57.23 2.73.12 3.02.72.79 1.16 1.8 1.16 3.04 0 4.35-2.65 5.3-5.17 5.59.36.31.68.92.68 1.85v2.74c0 .3.2.65.78.54A11.3 11.3 0 0 0 12 .7Z"/></svg>'
const iconLinkedin =
  '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M5.1 3.7A2.1 2.1 0 1 1 .9 3.7a2.1 2.1 0 0 1 4.2 0ZM1.1 8.1h4v12.8h-4V8.1Zm6.5 0h3.8v1.75h.05c.53-1 1.83-2.05 3.76-2.05 4.02 0 4.76 2.65 4.76 6.1v7h-4v-6.2c0-1.48-.03-3.38-2.06-3.38-2.07 0-2.38 1.61-2.38 3.27v6.31h-3.93V8.1Z"/></svg>'
const iconMail =
  '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M2.5 5.5h19v13h-19v-13Zm1.8 1.8 7.7 5.9 7.7-5.9H4.3Zm15.4 9.4V9.2L12 14.9 4.3 9.2v7.5h15.4Z"/></svg>'
fetch('/api/v1/content/profile/')
  .then(r => r.json())
  .then(p => {
    const links = [
      p.email &&
        `<a class="btn btn-primary social-btn" href="mailto:${p.email}">${iconMail}<span>Email ${p.email}</span></a>`,
      p.github_url &&
        `<a class="btn btn-ghost social-btn" href="${p.github_url}" target="_blank" rel="noreferrer">${iconGithub}<span>GitHub</span></a>`,
      p.linkedin_url &&
        `<a class="btn btn-ghost social-btn" href="${p.linkedin_url}" target="_blank" rel="noreferrer">${iconLinkedin}<span>LinkedIn</span></a>`,
      p.website_url &&
        `<a class="btn btn-ghost social-btn" href="${p.website_url}" target="_blank" rel="noreferrer"><span>Website</span></a>`,
      `<a class="btn btn-ghost social-btn" href="/resume/download/"><span>Resume</span></a>`
    ]
      .filter(Boolean)
      .join('')
    document.querySelector('#contactLinks').innerHTML = links
  })
