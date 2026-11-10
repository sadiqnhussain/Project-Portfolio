document.addEventListener('click', event => {
  const anchor = event.target.closest('a[href^="#"]')
  if (!anchor) return
  const target = document.querySelector(anchor.getAttribute('href'))
  if (target) {
    event.preventDefault()
    target.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
})

const topButton = document.querySelector('#backToTop')
if (topButton) {
  window.addEventListener(
    'scroll',
    () => topButton.classList.toggle('visible', window.scrollY > 420),
    { passive: true }
  )
  topButton.addEventListener('click', () =>
    window.scrollTo({ top: 0, behavior: 'smooth' })
  )
}
