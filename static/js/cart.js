var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'action:', action)
		console.log('USER:', user)
		if (user == 'AnonymousUser'){
			addCookeiItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}
function addCookeiItem(productId, action){
    console.log('bro is not authenticated');
    // Обработка добавления в корзину с учетом выбранного типа цены и количества
    var priceType = document.querySelector('input[name="price-type"]:checked').value;
    var quantity = document.getElementById('quantity-input').value;

    // Ваш код для добавления в корзину с использованием типа цены и количества
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 0 };
        }

        if (priceType === 'wholesale') {
            cart[productId]['quantity'] += 1; // Добавление одного товара при выборе оптовой цены
        } else if (priceType === 'box') {
            cart[productId]['quantity'] += parseInt(quantity); // Добавление количества для цены за ящик
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }

    console.log('Cart:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}
function updateUserOrder(productId, action){
    console.log('ye, bro is logged in')

    var url = '/update_item/'
    fetch(url, {
		method:'POST',
		headers:{
		    'Content-Type':'application/json',
		    'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'productId':productId, 'action':action})
	})
	.then((response) => {
	   return response.json();
	})
	.then((data) => {
	    console.log('data: ', data)
	    location.reload()
	});

}