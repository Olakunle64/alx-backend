const express = require('express');
import { createClient } from 'redis';
import { promisify } from 'util';

const listProducts = [
    {"itemId": 1, "itemName": "Suitcase 250", "price": 50, "initialAvailableQuantity": 4},
    {"itemId": 2, "itemName": "Suitcase 450", "price": 100, "initialAvailableQuantity": 10},
    {"itemId": 3, "itemName": "Suitcase 650", "price": 350, "initialAvailableQuantity": 2},
    {"itemId": 4, "itemName": "Suitcase 1050", "price": 550, "initialAvailableQuantity": 5}
]

function getItemById(id) {
    for (const product of listProducts) {
        if (product["itemId"] === id) return product
    }
}

const port = 1245;
const app = express();

app.get('/list_products', (req, res) => {
    res.json(listProducts)
})

const client = createClient();
client.on('error', (err) => {
    console.log("Redis client not connected to the server: " + err);
    });
client.on('connect', () => {
        console.log("Redis client connected to the server");
    });

const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

async function reserveStockById(itemId, stock) {
    try {
        const reply = await setAsync(itemId, stock)
    } catch(err) {
        console.log(err);
    } 
}

async function getCurrentReservedStockById(itemId) {
    try {
        const stock = await getAsync(itemId);
        return stock !== null ? parseInt(stock, 10) : null;
    } catch(err) {
        console.log(err);
    } 
}

app.get('/list_products/:itemId', (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const product = getItemById(itemId);
    if (!product) {
        return res.status(404).json({ status: 'Product not found' });
    } else {
        getCurrentReservedStockById(itemId).then((currentStock) => {
            product["currentQuantity"] = currentStock;
            res.json(product);
        })
    }
    
})

app.get('/reserve_product/:itemId', (req, res) => {
    const itemId = parseInt(req.params.itemId, 10);
    const product = getItemById(itemId);
    if (!product) {
        return res.status(404).json({ status: 'Product not found' });
    } else {
        getCurrentReservedStockById(itemId).then((currentStock) => {
            const currentQuantity = currentStock !== null ? currentStock : product.initialAvailableQuantity;
            if (currentQuantity >= 1) {
                reserveStockById(itemId, currentQuantity - 1).then(() => {
                    res.json({"status": "Reservation confirmed", "itemId": `${itemId}`});
                })
    
            } else {
                res.json({"status": "Not enough stock available", "itemId": `${itemId}`})
            }
        })
        
    }
})
app.listen(port)