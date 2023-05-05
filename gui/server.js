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
app.get('/addCamera', (req, res) => {
    res.sendFile(path.join(__dirname, 'src/addCamera.html'))
})

// Routes for CRUD
app.get('/saveSettings', (req, res) => {
    const data = req.query
    file.settings.rtsp = data.rtsp
    file.settings.program = data.program
    file.settings.website = data.website
    file.settings.delay = data.delay
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/index.html'))
})
app.get('/saveEmail', (req, res) => {
    file.email.password = req.query.emailPassword
    file.email.subject = req.query.emailSubject
    file.email.content = req.query.emailContent
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/email.html'))
})
app.get('/saveSms', (req, res) => {
    file.sms.secret = req.query.smsSecret
    file.sms.key = req.query.smsKey
    file.sms.number = req.query.smsNumber
    file.sms.text = req.query.smsText
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/sms.html'))
})
app.get('/add', (req, res) => {
    file.devices.cameras.push(
        {
            "name": req.query.name,
            "ip": req.query.ip,
            "relais": req.query.relais
        }
    )
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/cameras.html'));
})
app.get('/delete', (req, res) => {
    file.devices.cameras.splice(req.query.id, 1);
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    res.sendFile(path.join(__dirname, 'src/cameras.html'));
})

app.get('/data', (req, res) => {
    res.json(file)
})