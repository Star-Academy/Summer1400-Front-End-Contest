// CONFIG
const carGenerationSpeed = 1000;
const maximumCarsPerStreet = 4;
const carsScreenOffset = 100;

// ELEMENTS
const streetElements = {
    top: document.querySelector('.street--vertical.reverse'),
    right: document.querySelector('.street--horizontal'),
    bottom: document.querySelector('.street--vertical'),
    left: document.querySelector('.street--horizontal.reverse'),
};

const carsElement = document.querySelector('.cars');
const carElements = {
    top: document.querySelector('.car--top'),
    right: document.querySelector('.car--right'),
    bottom: document.querySelector('.car--bottom'),
    left: document.querySelector('.car--left'),
};

// GLOBAL VARIABLES
let intervalIds = {};
let cars = {
    top: [],
    right: [],
    bottom: [],
    left: [],
};

// UTILS
const moveCarToTheEnd = (direction, car, index) => {
    car.style.transition = `${direction} 1s ease-in-out ${index * 0.2}s`;
    car.style[direction] = `calc(100% + ${carElements[direction].clientHeight + carsScreenOffset}px)`;
};

// MAIN
const switchLight = (direction, color) => {
    if (color === 'red') {
        intervalIds[direction] = setInterval(() => {
            if (cars[direction].length >= maximumCarsPerStreet)
                return;
            
            const car = carElements[direction].cloneNode(true);
            car.style.transition = `${direction} 1s ease-in-out`;
            
            cars[direction].push({car, transitionEnd: false});
            carsElement.appendChild(car);
            
            const index = cars[direction].length - 1;
            
            car.addEventListener('transitionend', () => {
                if (cars[direction][index])
                    cars[direction][index].transitionEnd = true;
            }, {once: true});
            
            let position = -((index * 1.5) * carElements[direction].clientHeight);
            if (direction === 'top' || direction === 'bottom')
                position += streetElements[direction].clientHeight;
            else
                position += streetElements[direction].clientWidth;
            
            setTimeout(() => car.style[direction] = position + 'px');
        }, carGenerationSpeed);
    } else if (color === 'green') {
        clearInterval(intervalIds[direction]);
        
        cars[direction].forEach(({car, transitionEnd}, i) => {
            const callback = () => moveCarToTheEnd(direction, car, i);
            
            if (transitionEnd) callback();
            else car.addEventListener('transitionend', callback);
        });
        
        cars[direction] = [];
    }
};
