document.addEventListener('DOMContentLoaded', function () {
    function hideAllPanels() {
        const panels = document.querySelectorAll('.main-content');
        panels.forEach(panel => {
            panel.style.display = 'none';
        });
    }

    function showPanel(panelId) {
        hideAllPanels();
        const panel = document.getElementById(panelId);
        if (panel) {
            panel.style.display = 'block';
        }
    }

    document.getElementById('orders').addEventListener('click', function () {
        showPanel('orders-panel');
    });

    document.getElementById('profile-settings').addEventListener('click', function () {
        showPanel('profile-panel');
    });

    document.getElementById('user-statistics').addEventListener('click', function () {
        showPanel('user-statistics-panel');
    });

    if (userIsStaff) {
        document.getElementById('total-statistics').addEventListener('click', function () {
            showPanel('total-statistics-panel');
        });
    }

    showPanel('profile-panel');
});

document.addEventListener('DOMContentLoaded', function() {
        fetch('/orders/')
            .then(response => response.json())
            .then(data => {
                const ordersContainer = document.getElementById('orders-container');
                if (data.orders.length > 0) {
                    data.orders.forEach(order => {
                        const orderDiv = document.createElement('div');
                        orderDiv.classList.add('order-panel');
                        orderDiv.innerHTML = `
                            <h3>Замовлення №${order.id} - Статус: ${order.status}</h3>
                            <p>Дата створення: ${ order.created_at }</p>
                            <ul>
                                ${order.items.map(item => `
                                    <li>${item.product_name} - ${item.quantity} x $${item.total_price}</li>
                                `).join('')}
                            </ul>
                            <h4>Загальна сума: $${order.total_price}</h4>
                        `;
                        ordersContainer.appendChild(orderDiv);
                    });
                } else {
                    ordersContainer.innerHTML = '<p>У вас поки що немає замовлень.</p>';
                }
            });
});

document.addEventListener("DOMContentLoaded", function () {

    fetch("/get_customer_statistics/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("user-statistics-panel").style.display = "block";
            document.getElementById("user-total-orders").innerText = `Всі замовлення: ${data.total_orders}`;
            document.getElementById("user-total-spent").innerText = `Загальні витрати: ${data.total_spent}`;
            document.getElementById("user-total-items").innerText = `Кількість замовлених товарів: ${data.total_items}`;
        })
        .catch(error => console.error("Помилка завантаження статистики користувача:", error));

    if (userIsStaff) {
        fetch("/get_total_statistics/")
            .then(response => response.json())
            .then(data => {
                document.getElementById("total-statistics-panel").style.display = "block";
                document.getElementById("total-orders").innerText = `Всі замовлення: ${data.total_orders}`;
                document.getElementById("total-revenue").innerText = `Дохід: ${data.total_revenue}`;
                document.getElementById("total-items").innerText = `Кількість замовлених товарів: ${data.total_items}`;
            })
            .catch(error => console.error("Помилка завантаження загальної статистики:", error));
    }
});