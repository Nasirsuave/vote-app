const resultContainer = document.getElementById('result-container')
const displayContainer = document.getElementById('display-container')

resultContainer.addEventListener('submit',event =>{
    event.preventDefault();
    
    const urlDisplay = resultContainer.dataset.urlDisplay
    const xhr = new XMLHttpRequest()
    const formData = new FormData(resultContainer);

    xhr.open('POST',urlDisplay,true)

    xhr.onload = function() {
        if (xhr.status === 200) {
            // Success: Display the message returned by the server
            const response = JSON.parse(xhr.responseText);  // Assuming response is JSON
            console.log(response)
            const candidates = response.election_candidates;
            
            if(candidates.length>0){
                for(const candidate of candidates){
                    displayContainer.innerHTML += `<li>${candidate.name}</li>`;
                }
            }
            else if(candidates.length === 0){
                displayContainer.innerHTML += `<p>Result not available for online display</p>`;
            }
                  
            
        } 
        else {
            // Error: Something went wrong with the request
            displayContainer.innerHTML += `<p>Result not available for online display<p>`;  
        }
    };
    xhr.send(formData);
})