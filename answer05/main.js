// write your code here ...
// CONFIG
const URL = 'http://localhost:5000/';

const directions = ['top', 'right', 'bottom', 'left'];
const colors = ['red', 'yellow', 'green'];

const durationMultiplier = 1000;

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
    
    const initialRedLightDuration = timeline[direction][0].duration;
    timeline[direction][3].duration += initialRedLightDuration;
    timeline[direction] = timeline[direction].slice(1, 4);
    
    let timer = initialRedLightDuration;
    const countdown = () => {
        if (timer < 0) console.error('less than zero', direction);
        counters[direction].innerHTML = (timer--).toString();
    };
    
    setInterval(countdown, durationMultiplier);
    countdown();
    
    const changeLight = (color, duration) => {
        setTimeout(() => {
            for (const c of colors)
                lights[direction][c].classList.add('off');
            
            lights[direction][color].classList.remove('off');
            switchLight(direction, color);
        }, durationMultiplier);
        
        timer = duration;
    };
    
    changeLight('red', initialRedLightDuration);
    
    const interval = (timeOffset = 0) => {
        let elapsedTime = timeOffset;
        
        timeline[direction].forEach(({color, duration}) => {
            setTimeout(() => changeLight(color, duration), elapsedTime * durationMultiplier);
            elapsedTime += duration;
        });
    };
    
    interval(initialRedLightDuration);
    setTimeout(() => setInterval(interval, totalTime * durationMultiplier), initialRedLightDuration * durationMultiplier);
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
