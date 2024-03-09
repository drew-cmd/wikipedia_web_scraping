document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById("wikiForm");
  const responseDiv = document.getElementById('response');
  const radioYes = document.getElementById('radioYes');
  const radioNo = document.getElementById('radioNo');


  form.addEventListener('submit', function(event) {
    event.preventDefault();

    // Get the value of the 'wikilink' input field
    const wikilinkValue = document.getElementById('wikilink').value;

    // Determine whether 'radioYes' or 'radioNo' is checked
    let checkValue;
    if (radioYes.checked) {
      checkValue = 1;
    } else if (radioNo.checked) {
      checkValue = 0;
    } else {
      // Default value if neither radio button is checked
      checkValue = 0;
    }

    // Construct the query string
    const queryString = `wikilink=${encodeURIComponent(wikilinkValue)}&check=${encodeURIComponent(checkValue)}`;

    // Send the fetch request to the server asynchronously
    fetch('http://localhost:8000/server/process_form?' + queryString, {
      method: 'GET',
    })
    .then(function(response) {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(function(data) {
      responseDiv.innerHTML = data;
    })
    .catch(function(error) {
      console.error('There was a problem submitting the form:', error);
      responseDiv.innerHTML = 'An error occurred while submitting the form. Please try again later.';
    });
  });
});
