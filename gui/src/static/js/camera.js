const devices = document.getElementById("tableBody")

fetch('/dataCamera')
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
            devices.appendChild(row)
        }
    })