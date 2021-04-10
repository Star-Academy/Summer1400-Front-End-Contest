const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());

app.listen(5000, () => console.log('Listening on port 5000 ...'));

app.get('/', (req, res) => {
    const data = {
        'timeline': {
            top: [
                {light: 'red', time: 0},
                {light: 'green', time: 20},
                {light: 'yellow', time: 5},
                {light: 'red', time: 75},
            ],
            right: [
                {light: 'red', time: 25},
                {light: 'green', time: 20},
                {light: 'yellow', time: 5},
                {light: 'red', time: 50},
            ],
            bottom: [
                {light: 'red', time: 50},
                {light: 'green', time: 20},
                {light: 'yellow', time: 5},
                {light: 'red', time: 25},
            ],
            left: [
                {light: 'red', time: 75},
                {light: 'green', time: 20},
                {light: 'yellow', time: 5},
                {light: 'red', time: 0},
            ],
        },
    };
    
    res.send(data);
});
