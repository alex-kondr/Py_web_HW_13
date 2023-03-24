const list = async () => {
    accessToken = localStorage.getItem("accessToken")


    const response = await fetch("http://localhost:8000/api/contacts", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    })

    if (response.status === 200) {
        result = await response.json()
        console.log("result: =")
        console.log(result)

        for (el of result) {

            elementDivCard = document.createElement("div")
            elementDivCard.className = "card"
            elementDivCard.style = "width: 18rem"
            contacts.appendChild(elementDivCard)

            elementImg = document.createElement("img")
            elementImg.className = "card-img-top"
            elementImg.src = "/README.md"
            elementDivCard.appendChild(elementImg)

            elementDiv = document.createElement("div")
            elementDiv.className = "card-body"
            elementDivCard.appendChild(elementDiv)


            element = document.createElement("h5")
            element.className = 'card-title'
            element.innerHTML = `Name: ${el.first_name} ${el.last_name}`
            elementDivCard.appendChild(element)

            element = document.createElement("p")
            element.className = "card-text"
            element.innerHTML = `<b>Phone</b>: ${el.phone}`
            elementDivCard.appendChild(element)
            
            element = document.createElement("p")
            element.className = "card-text"
            element.innerHTML = `<b>Email</b>: ${el.email}`
            elementDivCard.appendChild(element)

            elementBtn = document.createElement("a")
            elementBtn.href = "#"
            elementBtn.className = "btn btn-primary"
            elementBtn.innerHTML = "Edit"
            elementDivCard.appendChild(elementBtn)

            elementBtn = document.createElement('a')
            elementBtn.href = '#'
            elementBtn.className = 'btn btn-success'
            elementBtn.innerHTML = 'Add'
            elementDivCard.appendChild(elementBtn)


        }
    }

    if (response.status === 401) {
        refresh()
    }
}


const refresh = async () => {
    refreshToken = localStorage.getItem("refreshToken")

    const response = await fetch("http://localhost:8000/api/auth/refresh_token", {
        method: "GET",
        headers: {
            Authorization: `Bearer ${refreshToken}`,
        },
    })

    if (response.status === 200) {
        result = await response.json()
        localStorage.setItem('accessToken', result.access_token)
        localStorage.setItem('refreshToken', result.refresh_token)

        list()
    }
}

list()