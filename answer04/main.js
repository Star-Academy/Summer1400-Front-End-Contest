const colors = [
    '#f02e08',
    '#0e38a1',
];

const helloMessage =  'Hello, Code-Star!';

// Write your code down here ...
const title = document.querySelector('#title');
const helloButton = document.querySelector('#hello-button');
const colorButton = document.querySelector('#color-button');

let colorIndex = 0;

helloButton.addEventListener('click', () => {
    title.innerHTML = helloMessage;
});

colorButton.addEventListener('click', () => {
    document.body.style.background = colors[(colorIndex++) % 2];
});
