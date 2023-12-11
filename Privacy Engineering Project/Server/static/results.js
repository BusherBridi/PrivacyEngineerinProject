document.addEventListener('DOMContentLoaded', function () {
    const headers = document.querySelectorAll('th');

    // Add click event listener to each header
    headers.forEach(header => {
        header.addEventListener('click', function () {
            // Toggle the 'selected' class on click
            this.classList.toggle('selected');

            // Display selected headers
            displaySelectedHeaders();

            // Recalculate and display K-Score
            displayKScore();
        });
    });

    // Function to display selected headers
    function displaySelectedHeaders() {
        const headers = document.querySelectorAll('th');  // Include this line
        const selectedHeaders = Array.from(headers)
            .filter(header => header.classList.contains('selected'))
            .map(header => header.textContent);

        // Update the content of the element with id 'selected-headers'
        const selectedHeadersElement = document.getElementById('selected-headers');
        if (selectedHeadersElement) {
            const title = selectedHeaders.length > 0 ? 'Selected Headers: ' : 'Selected Headers:';
            selectedHeadersElement.textContent = title + selectedHeaders.join(', ');

            // Show the Remove button if there are selected headers
            const removeButton = document.getElementById('remove-button');
            if (removeButton) {
                removeButton.style.display = selectedHeaders.length > 0 ? 'inline-block' : 'none';
            }
        }
    }

    // Function to calculate and display K-Score
    function displayKScore() {
        const kScore = calculateKScore();
        console.log('K-Score:', kScore);

        // Update the content of the element with id 'k-score'
        const kScoreElement = document.getElementById('k-score');
        if (kScoreElement) {
            kScoreElement.textContent = 'K-Score: ' + kScore;
        }
    }

    function calculateKScore() {
            const headers = document.querySelectorAll('th.selected');
            const columns = Array.from(headers).map(header => Array.from(headers).indexOf(header) + 1);
        
            const uniqueValuesList = columns.map(columnIndex => {
                const uniqueValues = new Set();
                const rows = document.querySelectorAll('tbody tr');
        
                rows.forEach(row => {
                    const value = row.querySelector(`td:nth-child(${columnIndex})`).textContent;
                    uniqueValues.add(value);
                });
        
                return uniqueValues.size;
            });
        
            console.log(uniqueValuesList);
        }
    

    // Remove button click event listener
    const removeButton = document.getElementById('remove-button');
    if (removeButton) {
        removeButton.addEventListener('click', function () {
            // Your logic to remove data based on selected headers goes here
            // ...

            // Optionally, clear selected headers and update display
            headers.forEach(header => header.classList.remove('selected'));
            displaySelectedHeaders();
            displayKScore();
        });
    }

    // Initial display of selected headers and K-Score
    displaySelectedHeaders();
    displayKScore();
});
