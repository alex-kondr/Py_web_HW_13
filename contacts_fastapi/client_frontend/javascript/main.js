const form = document.forms[0]

console.log(form)

form.addEventListener('submit', async event => {
  event.preventDefault()
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      username: form.username.value,
      password: form.password.value,
    }),
  })
  console.log(response)
  console.log(response.status, response.statusText)
  
  if (response.status === 200) {
    result = await response.json()
    localStorage.setItem("accessToken", result.access_token)
    localStorage.setItem("refreshToken", result.refresh_token)
    window.location = "../templates/listContacts.html"
  }
})

