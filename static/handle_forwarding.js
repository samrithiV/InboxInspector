// script.js

function confirmForwarding() {
    // Get the current timestamp
    const timestamp = Date.now();

    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    // Define the request parameters
    xhr.open('POST', '/confirm_forwarding', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Define the callback function when the request completes
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log(xhr.responseText); // Handle server response
        } else {
            console.error('Request failed:', xhr.status);
        }
    };

    // Convert timestamp to JSON format
    const data = JSON.stringify({ timestamp: timestamp });

    // Send the request with the timestamp data
    xhr.send(data);
}
