const castButton = document.querySelector('.cast-btn');
seeMore = document.querySelector('.see-more')
seeMoreIcon = document.querySelector('.see-more .icon')
const formContainer = document.querySelector('.form-container')
const completionMessage = document.querySelector('.completion-msg')

castButton.addEventListener('click',()=>{
    //  document.body.style.opacity = "0.6"
     completionMessage.style.opacity = "1"
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