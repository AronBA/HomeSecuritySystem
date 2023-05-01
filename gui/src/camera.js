const devices = document.getElementById("tableBody")

fetch("../../settings.json")
    .then(response => response.json())
    .then(json => {
        const cameras = json.devices.cameras
        for (let i = 0; i < cameras.length; i++) {
            const cam = document.createElement("tr")
            cam.innerHTML =
            `
                <th>${i + 1}</th>
                <td>${cameras[i].name}</td>
                <td>${cameras[i].ip}</td>
                <td>${cameras[i].relais.join()}</td>
                <td><a href=http://localhost:4000/delete?id=${i}><button class='btn btn-danger'>Delete</button></a></td>
            `
            devices.appendChild(cam)
        }
    })