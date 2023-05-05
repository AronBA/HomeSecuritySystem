const emailState = document.getElementById("emailState")
const emailInputs = document.querySelectorAll(".emailInput")

emailState.addEventListener('click', (e) => {
    emailInputs.forEach(input => {
        input.disabled = !e.target.checked
    })
})

fetch('/dataEmail')
    .then(response => response.json())
    .then(json => {
        console.log(json)
        document.getElementsByName()
    })