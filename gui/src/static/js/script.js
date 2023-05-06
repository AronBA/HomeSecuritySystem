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
                    <td><a href='/deleteCamera?id=${i}'><button class='btn btn-danger'>Delete</button></a></td>
                `
                document.getElementById("tableBody").appendChild(row)
            }
        })
}

function setAlarms() {
    fetch('/data?d=alarms')
        .then(response => response.json())
        .then(alarms => {
            for (let i = 0; i < alarms.length; i++) {
                const row = document.createElement("tr")
                row.innerHTML =
                    `
                <th>${i + 1}</th>
                <td>${alarms[i].name}</td>
                <td>${alarms[i].atr.join()}</td>
                <td><a href='/deleteAlarm?id=${i}'><button class='btn btn-danger'>Delete</button></a></td>
            `
                document.getElementById("tableBody").appendChild(row)
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
                    <td><a href='/deleteDevice?id=${i}'><button class='btn btn-danger'>Delete</button></a></td>
                `
                document.getElementById("tableBody").appendChild(row)
            }
        })
}