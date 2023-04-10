function openNav() {
    if (screen && screen.width > 800) {
        document.getElementById("myNav").style.width = "10%";
    }
    else {
        document.getElementById("myNav").style.width = "30%";
    }
}

function closeNav() 
{
    document.getElementById("myNav").style.width = "0%";
}

