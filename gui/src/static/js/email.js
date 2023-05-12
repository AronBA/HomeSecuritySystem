const emailState = document.getElementById("emailState")
const emailInputs = document.querySelectorAll(".emailInput")

emailState.addEventListener('click', (e) => disableFields(e.target.checked))
function disableFields(state) {
    emailInputs.forEach(input => {
        input.readOnly = !state
    })
}

fetch('/data?d=email')
    .then(response => response.json())
    .then(json => {
        emailInputs.forEach(input => {
            input.value = json[input.name]
        })
        if (json.state) emailState.checked = true
        else disableFields(false)
    })