const express = require('express')
const app = express()
const fs = require('fs')
const fileName = '../../settings.json'
const file = require(fileName)

app.listen(4000, () => {
    console.log('Server is running on port 4000')
})

app.get('/save', (req, res) => {
    const data = req.query
    file.settings.rtsp = data.rtsp
    file.settings.program = data.program
    file.settings.website = data.website
    file.settings.delay = data.delay
    file.email.emailPassword = data.emailPassword
    file.email.emailSubject = data.emailSubject
    file.email.emailContent = data.emailContent
    file.sms.smsSecret = data.smsSecret
    file.sms.smsKey = data.smsKey
    file.sms.smsNumber = data.smsNumber
    file.sms.smsText = data.smsText
    console.log(file)
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
    console.log(req.query)
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
})

app.get('/delete', (req, res) => {
    file.devices.cameras.splice(req.query.id, 1);
    fs.writeFile(fileName, JSON.stringify(file), (err) => {
        if (err) return console.log(err)
    })
})