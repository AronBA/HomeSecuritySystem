
function setDevices() {
    console.log("asdfajlösdf")
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
