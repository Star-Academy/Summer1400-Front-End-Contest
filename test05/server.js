const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());

app.listen(5000, () => console.log("Listening on port 5000 ..."));

app.get("/", (req, res) => {
    const data = {
    "timeline": {
        top: [
            {color: "red", duration: 0},
            {color: "green", duration: 1},
            {color: "yellow", duration: 1},
            {color: "red", duration: 6},
        ],
        right: [
            {color: "red", duration: 2},
            {color: "green", duration: 1},
            {color: "yellow", duration: 1},
            {color: "red", duration: 4},
        ],
        bottom: [
            {color: "red", duration: 4},
            {color: "green", duration: 1},
            {color: "yellow", duration: 1},
            {color: "red", duration: 2},
        ],
        left: [
            {color: "red", duration: 6},
            {color: "green", duration: 1},
            {color: "yellow", duration: 1},
            {color: "red", duration: 0},
        ],
    },
    };
    
    res.send(data);
});
