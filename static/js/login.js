const modeChoiceSection = document.querySelector('.mode-choice');
const cameraStreamSection = document.querySelector('.camera-stream');

const normalModeForm = document.querySelector('.normal-mode');
const faceModeForm = document.querySelector('.face-mode');

const normalModeButton = document.getElementById('normal');
const faceModeButton = document.getElementById('face');
const cameraButton = document.getElementById('camera');

normalModeButton.onclick = () => {
    modeChoiceSection.style.display = 'none';
    normalModeForm.style.display = 'block';
}

faceModeButton.onclick = () => {
    modeChoiceSection.style.display = 'none';
    faceModeForm.style.display = 'block';
}

cameraButton.onclick = () => {
    cameraStreamSection.innerHTML = `<img src="/video" alt="face stream" width="100%">`;
}