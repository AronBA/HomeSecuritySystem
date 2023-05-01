const emailState = document.getElementById("emailState")
const smsState = document.getElementById("smsState")
const emailInputs =  document.querySelectorAll(".emailInput")
const smsInputs =  document.querySelectorAll(".smsInput")

emailState.addEventListener('click', (e)=> {changeState(emailInputs, e.target.checked)})
smsState.addEventListener('click', (e)=> {changeState(smsInputs, e.target.checked)})

function changeState(list ,state) {
    list.forEach(item => {
        item.disabled = !state
    })
}

