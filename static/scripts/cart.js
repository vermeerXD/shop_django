 document.addEventListener("DOMContentLoaded", () => {
        initCartButtons();
    });

    function getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute('content') : null;
    }

    function closeModal() {
        document.getElementById("cartModal").style.display = "none";
    }

    function openModal() {
        fetch('/cart/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("Cart Data: ", data);

            let cartHtml = '';
            data.cart_items.forEach(item => {
                cartHtml += `
                    <div class="cart-item" data-item-id="${item.id}">
                        <img src="${item.product.image_url}" alt="${item.product.name}">
                        <div class="cart-item-details">
                            <strong>${item.product.name}</strong><br>
                            ${item.quantity} x $${item.product.price} = $${item.total}<br>
                            <span>Stock: ${item.stock}</span>
                        </div>
                        <div class="cart-item-actions">
                            <button class="remove-btn" data-item-id="${item.id}">Видалити</button>
                            <button class="change-qty-btn" data-item-id="${item.id}" data-action="increase">Збільшити</button>
                            <button class="change-qty-btn" data-item-id="${item.id}" data-action="decrease">Зменшити</button>
                        </div>
                    </div>
                `;
            });

            document.getElementById("cartItems").innerHTML = cartHtml;
            document.getElementById("totalPrice").innerHTML = `Сума: $${data.total_price}`;
            document.getElementById("cartModal").style.display = "block";

            initCartButtons();
        })
        .catch(error => console.error('Error:', error));
    }

    function initCartButtons() {
        document.querySelectorAll(".remove-btn").forEach(button => {
            button.addEventListener("click", function () {
                const cartItemId = this.getAttribute("data-item-id");
                removeFromCart(cartItemId);
            });
        });

        document.querySelectorAll(".change-qty-btn").forEach(button => {
            button.addEventListener("click", function () {
                const cartItemId = this.getAttribute("data-item-id");
                const action = this.getAttribute("data-action");
                changeQuantity(cartItemId, action);
            });
        });
    }

    function removeFromCart(cartItemId) {
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            alert('CSRF token missing. Please refresh the page.');
            return;
        }

        fetch(`/remove-from-cart/${cartItemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                openModal();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function changeQuantity(cartItemId, action) {
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            alert('CSRF token missing. Please refresh the page.');
            return;
        }

        fetch(`/change-quantity/${cartItemId}/${action}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                openModal();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }