import { createClient } from 'redis';
import { print } from 'redis';
import { promisify } from 'util';

const client = createClient();
client.on('error', (err) => {
    console.log("Redis client not connected to the server: " + err);
    });
client.on('connect', () => {
        console.log("Redis client connected to the server");
    });

// task 2
function setNewSchool(schoolName, value) {
    client.set(schoolName, value, (err, reply) => {
        if (err) {
            console.log(err);
        }
        print("Reply: " + reply);
    });
}

const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName) {
    try {
        const reply = await getAsync(schoolName)
        print(reply);
    } catch(err) {
        console.log(err);
    }  
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');