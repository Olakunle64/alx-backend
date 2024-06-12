
import { createClient } from 'redis';
import { promisify } from 'util';
const kue = require('kue');
const express = require('express');

const client = createClient();
client.on('error', (err) => {
    console.log("Redis client not connected to the server: " + err);
});
client.on('connect', () => {
    console.log("Redis client connected to the server");
});

// Set the initial number of available seats to 50
client.set('available_seats', 50, (err, reply) => {
    if (err) {
        console.log(err);
    }
});

// Set the reservationEnabled key to true
client.set('reservationEnabled', 'true', (err, reply) => {
    if (err) {
        console.log(err);
    }
});

const reserveSeat = (number) => {
    client.set('available_seats', number, (err, reply) => {
        if (err) {
            console.log(err);
        }
    });
}

// Promisify the get method of the client
const getAsync = promisify(client.get).bind(client);

const getAvailableSeats = async () => {
    try {
        const reply = await getAsync('available_seats');
        if (parseInt(reply) <= 0) {
            client.set('reservationEnabled', 'false', (err, reply) => {
                if (err) {
                    console.log(err);
                }
            });
        }
        return reply;
    } catch (err) {
        console.log(err);
    }
}

const queue = kue.createQueue();
const app = express();
const port = 1245;

app.get('/available_seats', async (req, res) => {
    try {
        const availableSeats = await getAvailableSeats();
        res.json({ "numberOfAvailableSeats": availableSeats });
    } catch (err) {
        res.status(500).json({ "error": err.message });
    }
});

app.get('/reserve_seat', async (req, res) => {
    try {
        const reservationEnabled = await getAsync('reservationEnabled');
        if (reservationEnabled === 'false') {
            res.json({ "status": "Reservations are blocked" });
        } else {
            const job = queue.create('reserve_seat', {}).save((err) => {
                if (err) {
                    res.json({ "status": "Reservation failed" });
                } else {
                    res.json({ "status": "Reservation in process" });
                }
            }).on('complete', () => {
                console.log(`Seat reservation job ${job.id} completed`);
            }).on('failed', (err) => {
                console.log(`Seat reservation job ${job.id} failed: ${err}`);
            });
        }
    } catch (err) {
        res.status(500).json({ "error": err.message });
    }
});

app.get('/process', (req, res) => {
    queue.process('reserve_seat', async (job, done) => {
        try {
            let availableSeats = await getAvailableSeats();
            availableSeats = parseInt(availableSeats, 10); // Ensure it's an integer
            if (availableSeats <= 0) {
                done(new Error('Not enough seats available'));
            } else {
                availableSeats -= 1;
                reserveSeat(availableSeats);
                if (availableSeats === 0) {
                    client.set('reservationEnabled', 'false', (err, reply) => {
                        if (err) {
                            console.log(err);
                        }
                    });
                }
                done();
            }
        } catch (err) {
            done(err);
        }
    });
    res.json({ "status": "Queue processing" });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});