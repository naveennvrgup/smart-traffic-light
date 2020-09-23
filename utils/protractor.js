// This will place a protractor png on the middle of screen
// so that we can get the direction of traffic light

// copy and place in chrome console 

let img=document.createElement('img')
let html=document.querySelector('html')
img.src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Rapporteur.svg/768px-Rapporteur.svg.png'
img.style='position:fixed;top:50vh;left:50vw;z-index:1000;width:400px;transform: translate(-50%,-50%);'
html.appendChild(img)