// Get the root element
var r = document.querySelector(':root');
function setTheme(textColour="white", contrast_bg="black", mild_bg= "#66a", med_bg= "#559", strong_bg= "#227") {

    // Set value of colour variables
    r.style.setProperty('--textColour', textColour);
    r.style.setProperty('--contrast_bg', contrast_bg);
    r.style.setProperty('--mild_bg', mild_bg);
    r.style.setProperty('--med_bg', med_bg);
    r.style.setProperty('--strong_bg', strong_bg);

    // Saving selection to session storage
    sessionStorage.setItem("textColour", textColour);
    sessionStorage.setItem("contrast_bg", contrast_bg);
    sessionStorage.setItem("mild_bg", mild_bg);
    sessionStorage.setItem("med_bg", med_bg);
    sessionStorage.setItem("strong_bg", strong_bg);
}

function getTheme(){
    
    // retrieve colours from session storage
    let textColour = sessionStorage.getItem("textColour");
    let contrast_bg = sessionStorage.getItem("contrast_bg");
    let mild_bg = sessionStorage.getItem("mild_bg");
    let med_bg = sessionStorage.getItem("med_bg");
    let strong_bg = sessionStorage.getItem("strong_bg");
    
    // set theme
    setTheme(textColour, contrast_bg, mild_bg, med_bg, strong_bg)    
}

if (sessionStorage.getItem("textColour")){      // if there's anything in session storage
    getTheme()                                  // retrieve the theme
}
else{
    setTheme()                                  // otherwise set it to default
}