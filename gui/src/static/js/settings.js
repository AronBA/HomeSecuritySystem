const settingsInputs = document.querySelectorAll(".settingsInput")

fetch('/dataSettings')
    .then(response => response.json())
    .then(json => {
        settingsInputs.forEach(input => {
            input.value = json[input.name]
        })
    })