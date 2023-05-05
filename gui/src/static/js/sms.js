const smsState = document.getElementById("smsState")
const smsInputs =  document.querySelectorAll(".smsInput")

smsState.addEventListener('click', (e) => {
    smsInputs.forEach(input => {
        input.disabled = !e.target.checked
    })
})