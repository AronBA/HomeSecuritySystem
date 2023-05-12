const express = require('express')
const app = express()
const crypto = require("crypto");
const path = require('path')
const fs = require('fs')
const fileName = '../settings.json'
const file = require(fileName)

app.listen(4000, () => {
    console.log('Server is running on port 4000')
})

app.use('/static', express.static(path.join(__dirname, 'src/static')))

app.get('/start', () => {
    const { spawn } = require('child_process')

    const pythonProcess = spawn('python', ['../Motiondetection/motiondetection.py'])

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    })
    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    })
    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    })
    file.id = pythonProcess.pid
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })

})
app.get('/stopp', () => {
    process.kill(file.id)
    file.id = ''
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    console.log('stopping software')
})

// Routes for pages
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/index.html'))
})
app.get('/cameras', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/cameras.html'))
})
app.get('/email', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/email.html'))
})
app.get('/sms', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/sms.html'))
})
app.get('/alarm', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/alarm.html'))
})
app.get('/device', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/device.html'))
})
app.get('/addCamera', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/addCamera.html'))
})
app.get('/addAlarm', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/addAlarm.html'))
})
app.get('/addDevice', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/addDevice.html'))
})

// Save to File
app.get('/saveSettings', (req, res) => {
    file.settings.program = req.query.program
    file.settings.website = req.query.website
    file.settings.delay = req.query.delay
    file.settings.threshold = req.query.threshold
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/index.html'))
})
app.get('/saveEmail', (req, res) => {
    file.email.state = req.query.hasOwnProperty('state')
    file.email.receiver = req.query.receiver
    file.email.password = req.query.password
    file.email.subject = req.query.subject
    file.email.content = req.query.content
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/email.html'))
})
app.get('/saveSms', (req, res) => {
    file.sms.state = req.query.hasOwnProperty('state')
    file.sms.secret = req.query.secret
    file.sms.key = req.query.key
    file.sms.number = req.query.number
    file.sms.text = req.query.text
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/sms.html'))
})

// Create and Delete
app.get('/createDevice', (req, res) => {
    file.devices.push(
        {
            "id": crypto.randomBytes(16).toString("hex"),
            "name": req.query.name,
            "ip": req.query.ip,
            "delay": req.query.delay
        }
    )
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/device.html'));
})
app.get('/createAlarm', (req, res) => {
    file.alarms.push(
        {
            "id": crypto.randomBytes(16).toString("hex"),
            "name": req.query.name,
            "email": req.query.hasOwnProperty('email'),
            "sms": req.query.hasOwnProperty('sms'),
            "devices": [...req.query.devices]
        }
    )
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/alarm.html'))
})
app.get('/createCamera', (req, res) => {
    file.cameras.push(
        {
            "name": req.query.name,
            "ip": req.query.ip,
            "alarms": [...req.query.alarms]
        }
    )
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/cameras.html'));
})
app.get('/deleteDevice', (req, res) => {
    const id = file.devices[req.query.id].id
    file.alarms.forEach(alarm => {
        alarm.devices = alarm.devices.filter(device => { return device !== id })
    })
    file.devices.splice(req.query.id, 1)
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/device.html'));
})
app.get('/deleteAlarm', (req, res) => {
    const id = file.alarms[req.query.id].id
    file.cameras.forEach(camera => {
        camera.alarms = camera.alarms.filter(alarm => { return alarm !== id })
    })
    file.alarms.splice(req.query.id, 1)
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/alarm.html'));
})
app.get('/deleteCamera', (req, res) => {
    file.cameras.splice(req.query.id, 1)
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/cameras.html'));
})

// Get DATA
app.get('/data', (req, res) => {
    res.json(file[req.query.d])
})