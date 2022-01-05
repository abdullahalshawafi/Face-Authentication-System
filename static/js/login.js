const modeChoiceSection = document.querySelector('.mode-choice');

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
    faceModeForm.style.display = 'flex';
}

cameraButton.onclick = () => {
    document.querySelector('.spinner-border').style.display = 'block';
    fetch('http://127.0.0.1:5000/video')
        .then(res => res.text())
        .then(data => {
            console.log(data);
            document.querySelector('.spinner-border').style.display = 'none';
            const out = document.createElement('p');
            out.innerText = data;
            faceModeForm.appendChild(out);
            fetch('http://127.0.0.1:5000/login-ajax', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: data })
            }).then(res => {
                if (res.status === 200) {
                    window.location.replace('http://127.0.0.1:5000/profile');
                } else {
                    alert("user not found");
                }
            });
        });
}