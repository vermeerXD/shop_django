function openReviewModal(button) {
    document.getElementById("productId").value = button.getAttribute("data-product-id");
    document.getElementById("reviewModal").style.display = "block";
}

function closeReviewModal() {
    document.getElementById("reviewModal").style.display = "none";
}

function submitReview() {
    const form = document.getElementById("reviewForm");
    const formData = new FormData(form);

    fetch('/submit-review/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCsrfToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Відгук успішно додано!");
            closeReviewModal();
        } else {
            alert("Помилка: " + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}
