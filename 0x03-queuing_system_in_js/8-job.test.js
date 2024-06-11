const kue = require('kue');
const queue = kue.createQueue();
const expect = require('chai').expect;

import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', function() {
    before(function() {
        console.log(queue.id)
        queue.testMode.enter();
    });

    afterEach(function() {
        queue.testMode.clear();
    });

    after(function() {
        queue.testMode.exit()
    });

    it('check the content of the queue', function() {
        createPushNotificationsJobs([{ phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' }], queue)
        console.log(queue.testMode.jobs.data);
    })
});