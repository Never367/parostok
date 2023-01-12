let orders = document.querySelectorAll('.order_row')

for (let order of orders) {
    order.onclick = function () {
        if (order.classList.contains('clicked')) {
            order.classList.remove('clicked')
            order.closest('.user_order').lastElementChild.classList.add('d-none')
            order.querySelector('.order_sum').classList.remove('d-none')
            for (let picture of order.querySelectorAll('.order_picture')) {
                picture.classList.remove('d-none')
            }
        } else {
            order.classList.add('clicked')
            order.closest('.user_order').lastElementChild.classList.remove('d-none')
            order.querySelector('.order_sum').classList.add('d-none')
            for (let picture of order.querySelectorAll('.order_picture')) {
                picture.classList.add('d-none')
            }
        }
    }
}
