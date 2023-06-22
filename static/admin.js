const urlGenerate = document.querySelectorAll('#url_generate');

// Loop through the buttons and add a click event listener to each one
urlGenerate.forEach(button => {
  button.addEventListener('click', () => {
    const rowId = button.dataset.id;
  const data = {
    id: rowId,
  };
  fetch('/my-flask-route', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.text())
  .then(html => {
    // Replace the current page with the new HTML page
    document.open();
    document.write(html);
    document.close();
  })
  .catch(error => {
    console.error(error);
    alert('Error fetching data: ' + error);
  });
  });
});