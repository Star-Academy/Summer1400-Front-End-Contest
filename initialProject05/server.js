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
            {color: "green", duration: 5},
            {color: "yellow", duration: 5},
            {color: "red", duration: 90},
        ],
        right: [
            {color: "red", duration: 10},
            {color: "green", duration: 25},
            {color: "yellow", duration: 5},
            {color: "red", duration: 60},
        ],
        bottom: [
            {color: "red", duration: 40},
            {color: "green", duration: 20},
            {color: "yellow", duration: 5},
            {color: "red", duration: 25},
        ],
        left: [
            {color: "red", duration: 65},
            {color: "green", duration: 30},
            {color: "yellow", duration: 5},
            {color: "red", duration: 0},
        ],
    },
    };
    
    res.send(data);
});
