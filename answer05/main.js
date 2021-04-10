// write your code here ...
const URL = 'http://localhost:5000/';

const screens = {
    top: document.querySelector('.screen--top'),
    right: document.querySelector('.screen--right'),
    bottom: document.querySelector('.screen--bottom'),
    left: document.querySelector('.screen--left'),
};

const lights = {
    top: {
        red: screens.top.getElementsByClassName('light--red')[0],
        yellow: screens.top.getElementsByClassName('light--yellow')[0],
        green: screens.top.getElementsByClassName('light--green')[0],
    },
    right: {
        red: screens.right.getElementsByClassName('light--red')[0],
        yellow: screens.right.getElementsByClassName('light--yellow')[0],
        green: screens.right.getElementsByClassName('light--green')[0],
    },
    bottom: {
        red: screens.bottom.getElementsByClassName('light--red')[0],
        yellow: screens.bottom.getElementsByClassName('light--yellow')[0],
        green: screens.bottom.getElementsByClassName('light--green')[0],
    },
    left: {
        red: screens.left.getElementsByClassName('light--red')[0],
        yellow: screens.left.getElementsByClassName('light--yellow')[0],
        green: screens.left.getElementsByClassName('light--green')[0],
    },
};

const simulateLight = (name, timeline) => {
    let totalTime = 0;
    timeline[name].forEach(({_, time}) => totalTime += +time);
    
    const interval = () => {
        let elapsedTime = 0;
        
        timeline[name].forEach(({light, time}) => {
            setTimeout(() => {
                lights[name].red.classList.add('off');
                lights[name].yellow.classList.add('off');
                lights[name].green.classList.add('off');
                
                lights[name][light].classList.remove('off');
            }, elapsedTime * 100);
            
            elapsedTime += time;
        });
    };
    
    interval();
    
    setInterval(interval, totalTime * 100);
};

const startSimulation = (timeline) => {
    simulateLight('top', timeline);
    simulateLight('right', timeline);
    simulateLight('left', timeline);
    simulateLight('bottom', timeline);
};

const startButton = document.querySelector('#start-button');
startButton.addEventListener('click', (e) => {
    e.target.disabled = true;
    
    fetch(URL)
        .then(res => res.json())
        .then(data => startSimulation(data.timeline))
        .catch(err => console.error(err));
});
