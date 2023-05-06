const express = require('express')
const app = express()
const path = require('path')
const fs = require('fs')
const fileName = '../settings.json'
const file = require(fileName)

app.listen(4000, () => {
    console.log('Server is running on port 4000')
})

app.use('/static', express.static(path.join(__dirname, 'src/static')))

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
            "name": req.query.name,
            "ip": req.query.ip,
        }
    )
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/device.html'));
})
app.get('/createAlarm', (req, res) => {
    console.log(req.query)
    file.alarms.push(
        {
            "name": req.query.name,
            "atr": req.query.atr
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
            "relais": [...req.query.relais]
        }
    )
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/cameras.html'));
})
app.get('/deleteDevice', (req, res) => {
    file.devices.splice(req.query.id, 1)
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/device.html'));
})
app.get('/deleteAlarm', (req, res) => {
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
    console.log(req.query)
    res.json(file[req.query.d])
})