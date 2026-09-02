document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alert notifications after 4 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // Quantity input auto-submit for cart detail table
  const quantitySelects = document.querySelectorAll('.cart-quantity-select');
  quantitySelects.forEach(select => {
    select.addEventListener('change', (e) => {
      e.target.closest('form').submit();
    });
  });

  // AJAX Add to Cart
  const addToCartForm = document.getElementById('add-to-cart-form');
  if (addToCartForm) {
    addToCartForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(this);
      
      fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          // Update cart badge
          const cartTotal = document.getElementById('cart-total');
          if (cartTotal) {
            cartTotal.textContent = data.cart_total_items;
            
            // Add a little pop animation
            cartTotal.style.transform = 'scale(1.5)';
            setTimeout(() => {
              cartTotal.style.transform = 'scale(1)';
            }, 300);
          }
          
          // Show toast notification
          showToast('Item added to cart!');
        }
      })
      .catch(error => console.error('Error adding to cart:', error));
    });
  }

  // AJAX Wishlist Toggle
  const wishlistForm = document.getElementById('wishlist-form');
  if (wishlistForm) {
    wishlistForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const formData = new FormData(this);
      
      fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.json())
      .then(data => {
        // Toggle button styling
        const btn = this.querySelector('button');
        const svg = btn.querySelector('svg');
        
        if (data.status === 'added') {
          svg.setAttribute('fill', 'currentColor');
          svg.style.color = 'var(--primary-color)';
          btn.innerHTML = btn.innerHTML.replace('Add to Wishlist', 'Saved to Wishlist');
        } else {
          svg.setAttribute('fill', 'none');
          svg.style.color = 'currentColor';
          btn.innerHTML = btn.innerHTML.replace('Saved to Wishlist', 'Add to Wishlist');
        }
        
        showToast(data.message);
      })
      .catch(error => console.error('Error toggling wishlist:', error));
    });
  }

  // Search Autocomplete
  const searchInput = document.getElementById('search-input');
  const resultsDropdown = document.getElementById('autocomplete-results');
  
  if (searchInput && resultsDropdown) {
    let debounceTimer;
    
    searchInput.addEventListener('input', function() {
      clearTimeout(debounceTimer);
      const query = this.value.trim();
      
      if (query.length < 2) {
        resultsDropdown.classList.remove('active');
        return;
      }
      
      debounceTimer = setTimeout(() => {
        fetch(`/search-autocomplete/?q=${encodeURIComponent(query)}`)
          .then(response => response.json())
          .then(data => {
            if (data.results && data.results.length > 0) {
              resultsDropdown.innerHTML = '';
              data.results.forEach(item => {
                const a = document.createElement('a');
                a.href = item.url;
                a.className = 'autocomplete-item';
                a.textContent = item.name;
                resultsDropdown.appendChild(a);
              });
              resultsDropdown.classList.add('active');
            } else {
              resultsDropdown.innerHTML = '<div class="autocomplete-item" style="color: var(--text-muted);">No products found</div>';
              resultsDropdown.classList.add('active');
            }
          })
          .catch(error => console.error('Autocomplete error:', error));
      }, 300);
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !resultsDropdown.contains(e.target)) {
        resultsDropdown.classList.remove('active');
      }
    });
  }

  // Helper for Toasts
  function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'alert alert-success';
    toast.style.position = 'fixed';
    toast.style.bottom = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.style.boxShadow = 'var(--shadow-lg)';
    toast.innerHTML = `<span>${message}</span>`;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.4s ease';
      setTimeout(() => toast.remove(), 400);
    }, 3000);
  }
});
