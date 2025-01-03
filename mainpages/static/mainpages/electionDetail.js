const castButton = document.querySelector('.cast-btn');
seeMore = document.querySelector('.see-more')
seeMoreIcon = document.querySelector('.see-more .icon')
const formContainer = document.querySelector('.form-container')
const completionMessage = document.querySelector('.completion-msg')
const messageContainer = document.querySelector('.completion-msg .message-container')


castButton.addEventListener('click',()=>{
    //  document.body.style.opacity = "0.6"
     completionMessage.style.opacity = "1"
     //document.body.style.opacity = ".4"
     //completionMessage.style.top = "24rem"
     completionMessage.classList.add('moved')
})

seeMore.addEventListener('click',()=>{
     // formContainer.style.opacity = "0"
     // formContainer.style.height = "0vh"
     //const formHeight = window.getComputedStyle(formContainer).height;
     if (formContainer.style.height === "0vh") {
          // Expand the form container
          formContainer.style.height = "28vh";
          formContainer.style.opacity = "1";
          // Change the icon to "up"
          seeMoreIcon.classList.remove("fa-chevron-down");
          seeMoreIcon.classList.add("fa-chevron-up");
        }
        else {
          // Collapse the form container
          formContainer.style.height = "0vh";
          formContainer.style.opacity = "0";
          // Change the icon to "down"
          seeMoreIcon.classList.remove("fa-chevron-up");
          seeMoreIcon.classList.add("fa-chevron-down");
        }
})

formContainer.addEventListener('submit',event =>{
    event.preventDefault();
    
    const electionId = formContainer.dataset.electionId; 
    const casturl = formContainer.dataset.castUrl;
    const formData = new FormData(formContainer);

  //   for (const [key, value] of formData.entries()) {
  //     console.log(`${key}: ${value}`);
  // }
    const xhr = new XMLHttpRequest();

    //const url = "{% url 'cast-vote' election.id %}"
    //.replace('election.id', electionId);
    xhr.open("POST", casturl, true);

    xhr.onload = function() {
      if (xhr.status === 200) {
          // Success: Display the message returned by the server
          const response = JSON.parse(xhr.responseText);  // Assuming response is JSON
          messageContainer.innerHTML = `${response.message}`;
          messageContainer.classList.add('message-success')


      } else {
          // Error: Something went wrong with the request
          messageContainer.innerHTML = "Something went wrong. Please try again later.";
          messageContainer.classList.add('message-fail')

      }
  };
  xhr.send(formData);
})