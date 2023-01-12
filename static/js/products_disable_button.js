let tooltipElem;

    document.onmouseover = function(event) {
      let target = event.target;

      // if we have a clue...
      let tooltipHtml = target.dataset.tooltip;
      if (!tooltipHtml) return;

      // ...create an element for hint

      tooltipElem = document.createElement('div');
      tooltipElem.className = 'tooltip_product_disable';
      tooltipElem.innerHTML = tooltipHtml;
      document.body.append(tooltipElem);

      // position it on top of the annotated element (top-center)
      let coords = target.getBoundingClientRect();

      let left = coords.left + (target.offsetWidth - tooltipElem.offsetWidth) / 2;
      if (left < 0) left = 0; // do not drive over the left edge of the window

      let top = coords.top - tooltipElem.offsetHeight - 5;
      if (top < 0) { // if the tooltip does not fit on top, then display it on the bottom
        top = coords.top + target.offsetHeight + 5;
      }

      tooltipElem.style.left = left + 'px';
      tooltipElem.style.top = top + 'px';
    };

    document.onmouseout = function(e) {

      if (tooltipElem) {
        tooltipElem.remove();
        tooltipElem = null;
      }

    };
