const escapeButton = document.getElementById("escape-button");
let orginalHeight = escapeButton.clientHeight;
let orginalWidth = escapeButton.clientWidth;
let run = true;

escapeButton.addEventListener("mouseover", () => {
  if(run) {
    const pageX = window.innerWidth - 250 - escapeButton.clientWidth;
    const pageY = window.innerHeight - 250 - escapeButton.clientHeight;
    const randomPageX = Math.floor(Math.random() * pageX);
    const randomPageY = Math.floor(Math.random() * pageY);
    escapeButton.style.position = 'absolute';
    escapeButton.style.zIndex = '2';
    escapeButton.style.left = `${randomPageX}px`;
    escapeButton.style.top = `${randomPageY}px`;
    const Button = document.getElementById("escape-button");
    let newHeight = Button.clientHeight - 2;
    let newWidth = Button.clientWidth - 10;
    Button.style.height = newHeight + "px";
    Button.style.width = newWidth + "px";
    if (newWidth < 1) {
        Button.innerHTML = "";
        alert('یک دکمه پرداخت معذرت');
        escapeButton.style.position = 'static';
        escapeButton.style.zIndex = '0';
        Button.style.height = orginalHeight + "px";
        Button.style.width = orginalWidth + "px";
        Button.innerHTML = 'پرداخت';
        run = false;
    }
  }
});