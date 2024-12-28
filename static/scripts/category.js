const categorySlug = document.body.getAttribute('data-category-slug');

function applySorting() {
    if (typeof categorySlug === 'undefined' || !categorySlug) {
        console.error('categorySlug is not defined or empty');
        return;
    }

    const sortBy = document.getElementById('sortBy').value;
    const [sortField, sortOrder] = sortBy.split('-');
    const brandId = document.getElementById('brandFilter') ? document.getElementById('brandFilter').value : '';

    let url = `/products/sort/${categorySlug}/?sort_by=${sortField}&order=${sortOrder}`;
    if (brandId) {
        url += `&brand=${brandId}`;
    }

    console.log('URL:', url);

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch sorted products');
            }
            return response.json();
        })
        .then(data => {
            const productList = document.getElementById('product-list');
            productList.innerHTML = '';

            if (data.products && data.products.length > 0) {
                const seenProducts = new Set();
                const uniqueProducts = [];

                data.products.forEach(product => {
                    if (!seenProducts.has(product.id)) {
                        seenProducts.add(product.id);
                        uniqueProducts.push(product);
                    }
                });

                uniqueProducts.forEach(product => {
                    const productItem = `
                        <div class="product-item">
                            <a href="/${product.category_slug}/${product.slug}/">
                                <img src="${product.image || '/static/images/placeholder.jpg'}" alt="${product.name}">
                                <h3>${product.name}</h3>
                                <p class="price">$${product.price}</p>
                            </a>
                        </div>
                    `;
                    productList.innerHTML += productItem;
                });
            } else {
                productList.innerHTML = '<p>Нічого не знайдено.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching sorted products:', error);
        });
}
