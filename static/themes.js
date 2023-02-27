// Get the root element
var r = document.querySelector(':root');
function setTheme(textColour="red", contrast_bg="black", mild_bg= "#66a", med_bg= "#559", strong_bg= "#227") {

    // Set value of colour variables
    r.style.setProperty('--textColour', textColour);
    r.style.setProperty('--contrast_bg', contrast_bg);
    r.style.setProperty('--mild_bg', mild_bg);
    r.style.setProperty('--med_bg', med_bg);
    r.style.setProperty('--strong_bg', strong_bg);
}