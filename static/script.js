document.addEventListener('DOMContentLoaded', () => {
    const createBtn = document.getElementById('createBtn');
    const wordInput = document.getElementById('wordInput');
    const statusDiv = document.getElementById('status');

    createBtn.addEventListener('click', async () => {
        const word = wordInput.value.trim();

        if (!word) {
            updateStatus('Please enter a word or phrase.', 'danger');
            return;
        }

        // Disable button and show loading state
        createBtn.disabled = true;
        createBtn.textContent = 'Creating...';
        statusDiv.innerHTML = ''; // Clear previous status

        try {
            // Call the Python API
            const result = await window.pywebview.api.create_card(word);

            if (result.status === 'success') {
                updateStatus(result.message, 'success');
                wordInput.value = ''; // Clear input on success
            } else {
                updateStatus(result.message, 'danger');
            }
        } catch (e) {
            updateStatus('An unexpected error occurred.', 'danger');
            console.error(e);
        }

        // Re-enable button
        createBtn.disabled = false;
        createBtn.textContent = 'Create Card';
    });

    function updateStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = `mt-3 text-center text-${type}`;
    }
});
