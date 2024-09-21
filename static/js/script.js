// Image preview functionality
document.getElementById('file-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('preview');
            preview.innerHTML = `<img src="${e.target.result}" alt="Image Preview" class="img-fluid" style="max-width: 100%;">`;
        };
        reader.readAsDataURL(file);
    }
});

// Close button functionality for processed image
document.getElementById('close-btn')?.addEventListener('click', function() {
    const processedImageContainer = document.getElementById('processed-image-container');
    if (processedImageContainer) {
        processedImageContainer.style.display = 'none'; // or use 'remove()' to completely remove the element
    }
});

// Reset functionality to clear the preview
document.querySelector('form').addEventListener('reset', function() {
    const previewContainer = document.getElementById('preview');
    previewContainer.innerHTML = ''; // Clear the preview on form reset
});
