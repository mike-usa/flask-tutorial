onLoad()

function onLoad(){
  const body = document.querySelector('body')
  const isEnabled = localStorage.getItem('dark-mode') == 'true'

  body.classList.toggle('dark', isEnabled)
}

function toggleMode(){
  const body = document.querySelector('body')
  body.classList.toggle('dark')
  localStorage.setItem('dark-mode', body.classList.contains('dark'))
}

function useInternalLink(){
  location.href = this.event.target.querySelector('a').href
}