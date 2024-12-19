document.getElementById('orders').addEventListener('click', function() {
        document.getElementById('profile-panel').style.display = 'none';
        document.getElementById('orders-panel').style.display = 'block';
    });

    document.getElementById('profile-settings').addEventListener('click', function() {
        document.getElementById('orders-panel').style.display = 'none';
        document.getElementById('profile-panel').style.display = 'block';
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