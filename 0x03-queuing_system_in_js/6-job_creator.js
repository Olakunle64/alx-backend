const kue = require('kue')

const queue = kue.createQueue()
const job = queue.create('push_notification_code', {
    phoneNumber: '07062869135',
    message: 'Islam is the best religion',
  }).save((err) => {
    if (!err) console.log(`Notification job created: ${job.id}`)
        else console.log(`Notification job failed: ${err}`)
  }).on('complete', () => console.log('Notification job completed'));