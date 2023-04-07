const form = document.forms[0]

console.log(form)

form.addEventListener('submit', async event => {
    event.preventDefault()
    
    accessToken = localStorage.getItem('accessToken')

  const response = await fetch('http://localhost:8000/api/contacts/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
    },
    body: JSON.stringify({
      first_name: form.first_name.value,
      last_name: form.last_name.value,
      phone: form.phone.value
    })
  })

  if (response.status === 200) {
    result = await response.json()
    localStorage.setItem('accessToken', result.access_token)
    localStorage.setItem('refreshToken', result.refresh_token)
  }
  
  if (response.status === 201) {
    window.location = '../templates/listContacts.html'  
  }
    
    if (response.status === 401) {
        refresh()
    }
})


const refresh = async () => {
  refreshToken = localStorage.getItem('refreshToken')

  const response = await fetch('http://localhost:8000/api/auth/refresh_token', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${refreshToken}`
    }
  })

  if (response.status === 200) {
    result = await response.json()
    localStorage.setItem('accessToken', result.access_token)
    localStorage.setItem('refreshToken', result.refresh_token)
  }
}

