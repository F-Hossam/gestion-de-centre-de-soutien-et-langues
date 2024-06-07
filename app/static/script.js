function togglePopup(i) {
    document.getElementById(`popup-${i}`).classList.toggle("active");
}

function togglePopupAbout(i) {
    document.getElementById(`popup-about-${i}`).classList.toggle("active");
}

function toggleGroupe(i) {
    document.getElementById(`groupe-about-${i}`).classList.toggle("active");
}

function toggleSeance(i) {
    document.getElementById(`seance-about-${i}`).classList.toggle("active");
}


function fetchFormation() {
    fetch('/toggle_button', { method: 'POST' })
}

function toggleAbsent(i){
    var present = document.getElementById(`present-seance-${i}`);
    present.style.backgroundColor = 'green';
    
    var pTag = document.getElementById(`solde-etudiant-${i}`);
    var pValue = pTag.textContent;
    if (pValue == 0){
        var activePayer = document.getElementById(`payer-seance-${i}`);
        activePayer.disabled = false;
        activePayer.style.backgroundColor = '#67729D';
    }

    var presentInput = document.getElementById(`etudiant-present-${i}`);
    presentInput.value = '1'; 
    
}

function togglePayer(i){
    var payerInput = document.getElementById(`payer-etudiant-${i}`);
    payerInput.value = '1'; 
    
}

