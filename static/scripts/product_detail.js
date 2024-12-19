function changeMainImage(src) {
            document.getElementById('main-image').src = src;
}

function addToCart(productId) {
    fetch(`/add-to-cart/${productId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Товар успішно додано до кошика.`);
        } else {
            console.error('Server returned error:', data);
            alert(`Помилка: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Network or parsing error:', error);
        alert('Виникла помилка при додаванні товару до кошика. Спробуйте пізніше.');
    });
}