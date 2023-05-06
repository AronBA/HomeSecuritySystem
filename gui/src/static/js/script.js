function setSettings() {
    fetch('/data?d=settings')
        .then(response => response.json())
        .then(json => {
            document.querySelectorAll(".settingsInput").forEach(input => {
                input.value = json[input.name]
            })
        })
}

function setCameras() {
    fetch('/data?d=cameras')
        .then(response => response.json())
        .then(cameras => {
            for (let i = 0; i < cameras.length; i++) {
                const row = document.createElement("tr")
                row.innerHTML =
                    `
                    <th>${i + 1}</th>
                    <td>${cameras[i].name}</td>
                    <td>${cameras[i].ip}</td>
                    <td>${cameras[i].relais.join()}</td>
                    <td><a href='/deleteCamera?id=${i}'><button class='btn btn-danger'><i class="bi bi-trash3"></i></button></a></td>
                `
                document.getElementById("tableBody").appendChild(row)
            }
        })
}

function setAlarms() {
    let devices
    fetch('/data?d=devices')
        .then(response => response.json())
        .then(json => devices = json)
    fetch('/data?d=alarms')
        .then(response => response.json())
        .then(alarms => {
            const tableBody = document.getElementById("tableBody")
            for (let i = 0; i < alarms.length; i++) {
                const row = document.createElement("tr")
                let devicesString = []
                alarms[i].devices.forEach(device => {
                    const dev = devices.find(d => d.id == device)
                    devicesString.push(`<span title='${dev.ip}'>${dev.name}</span>`)
                })
                row.innerHTML =
                    `
                <th>${i + 1}</th>
                <td>${alarms[i].name}</td>
                <td>${alarms[i].email ? '<i class="bi bi-check-lg"></i>' : '<i class="bi bi-x-lg"></i>'}</td>
                <td>${alarms[i].sms ? '<i class="bi bi-check-lg"></i>' : '<i class="bi bi-x-lg"></i>'}</td>
                <td>${devicesString.join(', ')}</td>
                <td><a href='/deleteAlarm?id=${i}'><button class='btn btn-danger'><i class="bi bi-trash3"></i></button></a></td>
            `
                tableBody.appendChild(row)
            }
        })
}

function setDevices() {
    fetch('/data?d=devices')
        .then(response => response.json())
        .then(devices => {
            for (let i = 0; i < devices.length; i++) {
                const row = document.createElement("tr")
                row.innerHTML =
                    `
                    <th>${i + 1}</th>
                    <td>${devices[i].name}</td>
                    <td>${devices[i].ip}</td>
                    <td><a href='/deleteDevice?id=${i}'><button class='btn btn-danger'><i class="bi bi-trash3"></i></button></a></td>
                `
                document.getElementById("tableBody").appendChild(row)
            }
        })
}

function setAddAlarm() {
    fetch('/data?d=devices')
        .then(response => response.json())
        .then(devices => {
            let options = ""
            devices.forEach(device => {
                options += `<option value='${device.id}' data-name='${device.name}'>${device.name}</option>`
            })
            document.getElementById('devices').innerHTML = options
        })
}