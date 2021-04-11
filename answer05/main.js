// write your code here ...
// CONFIG
const URL = 'http://localhost:5000/';

const directions = ['top', 'right', 'bottom', 'left'];
const colors = ['red', 'yellow', 'green'];

// ELEMENTS
const screens = {};
const counters = {};
const lights = {};

for (const direction of directions) {
    screens[direction] = document.querySelector(`.screen--${direction}`);
    counters[direction] = screens[direction].querySelector('.counter');
    
    lights[direction] = {};
    for (const color of colors)
        lights[direction][color] = screens[direction].querySelector(`.light--${color}`);
}

// FUNCTIONS
const simulateLight = (direction, timeline) => {
    let totalTime = 0;
    timeline[direction].forEach(({_, duration}) => totalTime += +duration);
    
    let timer;
    setInterval(() => {
        if (timer < 0)
            console.log('less than zero', direction);
        
        counters[direction].innerHTML = (timer--).toString();
    }, 100);
    
    const interval = () => {
        let elapsedTime = 0;
        
        timeline[direction].forEach(({color, duration}) => {
            setTimeout(() => {
                for (const color of colors)
                    lights[direction][color].classList.add('off');
                
                lights[direction][color].classList.remove('off');
                switchLight(direction, color);
                
                timer = duration;
            }, elapsedTime * 100);
            
            elapsedTime += duration;
        });
    };
    
    interval();
    setInterval(interval, totalTime * 100);
};

const startSimulation = (timeline) => {
    for (const direction of directions)
        simulateLight(direction, timeline);
};

// MAIN
const startButton = document.querySelector('#start-button');
startButton.addEventListener('click', (e) => {
    e.target.disabled = true;
    
    fetch(URL)
        .then(res => res.json())
        .then(data => startSimulation(data.timeline))
        .catch(err => console.error(err));
});
