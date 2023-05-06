const devices = document.getElementById("tableBody")

fetch('/dataAlarm')
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
            devices.appendChild(row)
        }
    })