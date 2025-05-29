
const userIdElement = document.getElementById('user-id');
const userId = userIdElement.dataset.userId
const displayNotif = document.getElementById('display-notification')// Place this function in your main JavaScript file (e.g., app.js or notifications.js)
// or directly within a <script> tag in your HTML, outside of any specific DOMContentLoaded listeners
// so it's defined and ready when your WebSocket message arrives.

/**
 * Calculates the time difference and formats it as "X minutes/hours/days ago".
 * @param {string} createdAtIsoString The ISO 8601 timestamp string (e.g., "2025-05-26T13:50:00Z").
 * @returns {string} The formatted time string.
 */
function formatTimeAgo(createdAtIsoString) {
    // 1. Create a Date object from the received ISO string.
    //    JavaScript's Date constructor can parse ISO 8601 strings (with 'Z' or timezone offset) correctly.
    const createdDate = new Date(createdAtIsoString);

    // 2. Get the current time.
    const now = new Date();

    // 3. Calculate the difference in milliseconds.
    const diffMs = now.getTime() - createdDate.getTime();

    // 4. Convert milliseconds to minutes, hours, and days.
    const diffMinutes = Math.round(diffMs / (1000 * 60));
    const diffHours = Math.round(diffMs / (1000 * 60 * 60));
    const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

    // 5. Apply conditional logic to return the appropriate string.
    if (diffMinutes < 1) {
        return "Just now";
    } else if (diffMinutes < 60) {  //this condition  should always come before the condition that follows it 
        return `${diffMinutes} minute${diffMinutes === 1 ? '' : 's'} ago`;
    } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`;
    } else if (diffDays < 7) {
        return `${diffDays} day${diffDays === 1 ? '' : 's'} ago`;
    } else {
        // Fallback for older notifications: display the actual date
        // Adjust 'en-US' and options as per your locale/preference
        return createdDate.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
}



const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
const wsPath = wsScheme + '://' + window.location.host + '/ws/notify/' ; //Define a websocket url
const notificationSocket = new WebSocket(wsPath);

notificationSocket.onopen = function(e) {
    console.log("Connection open!");
};

notificationSocket.onmessage = function(e) {
   
    const data = JSON.parse(e.data);
    //{message:"SOmething here"}

    // {
    //     event: {
    //         type: 'notification.message', // This is usually the handler function name
    //         message: 'Welcome to Election X!',
    //         election_id: 456,
    //         election_name: 'My Awesome Election'
    //     }
    // }
    //to get the message value data.event.message
    

    const message = data.event.message;
    const created_at = formatTimeAgo(data.event.created_at);
    // Display the notification (e.g., using a toast library, or by updating a div)  

    const newButton = document.createElement('button')
    const newDiv = document.createElement('div')
    const newIcon = document.createElement('i')

    const bigDiv = document.createElement('div')
    //displayNotif.appendChild
    
    newDiv.innerHTML = `
    <h3  class="font-bold">Election Update</h3>
    <p>${created_at}</p>
    <p>${message}</p>
`;

    newButton.textContent = "View"


    bigDiv.appendChild(newIcon)
    bigDiv.appendChild(newDiv)
    bigDiv.appendChild(newButton) 
    
    newDiv.classList.add('styleNewDiv')
    bigDiv.classList.add('styleBigDiv')
    newButton.classList.add('styleNewButton')

    displayNotif.prepend(bigDiv)

};

notificationSocket.onclose = function(e) {
    console.log("Connection closed!");
};

notificationSocket.onerror = function(e){
    console.error("Socket Error",e)
}
