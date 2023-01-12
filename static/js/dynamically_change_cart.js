$(document).ready(function() {

        let a = document.cookie.split(';');
        let csrf_token = ''
        for (i = 0; i < a.length; i++) {
            let b = a[i].split('=')
            b[0] = b[0].replace(/\s+/g, '')
            if (b[0] === 'csrftoken') {
                csrf_token = b[1]
            }
        }
        let fadeTime = 300;

        $('.pass-quantity input').change(function() {
          let product_id = $(this).data('product_id')
          let product_age = $(this).data('product_age')
          let product_container = $(this).data('product_container')
          updateQuantity(this, product_id, product_age, product_container);
        });

        $('.remove-item button').click(function() {
          let product_id = $(this).data('product_id')
          let product_age = $(this).data('product_age')
          let product_container = $(this).data('product_container')
          removeItem(this, product_id, product_age, product_container);
        });


        /* Recalculate cart */
        function recalculateCart() {
          let total = 0;
          let total_length = 0;

          /* Sum up row totals */
          $('.item').each(function() {
            total += parseInt($(this).children().children('.product-line-price').text());
            total_length += parseInt($(this).children().children().children('.pass-quantity input').val());
          });

          /* Update totals display */
          $('.totals-value').fadeOut(fadeTime, function() {
            $('.cart-total').html(total + ' грн');
            $('.cart-total-length').html(total_length);
            if (total_length === 0) {
              $('.totals').fadeOut(fadeTime);
              $('.cart-total-length').hide();
              $('.cart-empty').show();
            } else {
              $('.checkout').fadeIn(fadeTime);
            }
            $('.totals-value').fadeIn(fadeTime);
          });
        }

        /* Update quantity */
        function updateQuantity(quantityInput, product_id, product_age, product_container) {
          /* Calculate line price */
          let productRow = $(quantityInput).parent().parent();
          let price = parseInt(productRow.children('.product-price').text());
          let quantity = $(quantityInput).val();
          if (quantity > 999) {
              quantity = 999
          }
          if (quantity < 1) {
              quantity = 1
          }
          let linePrice = price * quantity;

          /* Update line price display and recalculate cart totals */
          productRow.children('.product-line-price').each(function() {
            $(this).fadeOut(fadeTime, function() {
              $(this).text(linePrice.toFixed() + ' грн');
              recalculateCart();
              $(this).fadeIn(fadeTime);

              $.ajax({
                headers: {"X-CSRFToken": csrf_token},
                url: 'recalculate/' + product_id + '/' + product_age + '/' + product_container + '/' + quantity,
                type: 'POST',
            })
            });
          });
        }

        /* Remove item from cart */
        function removeItem(removeButton, product_id, product_age, product_container) {
          /* Remove row from DOM and recalculate cart total */
          let productRow = $(removeButton).parent().parent().parent();
          productRow.slideUp(fadeTime, function() {
            productRow.remove();
            recalculateCart();

            $.ajax({
                headers: {"X-CSRFToken": csrf_token},

                url: 'remove/' + product_id + '/' + product_age + '/' + product_container,
                type: 'POST'
            })
          });
        }

      });