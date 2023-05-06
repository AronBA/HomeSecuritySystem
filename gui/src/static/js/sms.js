const smsState = document.getElementById("smsState")
const smsInputs = document.querySelectorAll(".smsInput")

smsState.addEventListener('click', (e) => disableFields(e.target.checked))
function disableFields(state) {
    smsInputs.forEach(input => {
        input.readOnly = !state
    })
}

fetch('/data?d=sms')
    .then(response => response.json())
    .then(json => {
        smsInputs.forEach(input => {
            input.value = json[input.name]
        })
        if (json.state) smsState.checked = true
        else disableFields(false)
    })