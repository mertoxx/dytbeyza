// static/js/main.js

$(document).ready(function() {
    
    // Back to Top Button
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#backToTop').fadeIn();
        } else {
            $('#backToTop').fadeOut();
        }
    });
    
    $('#backToTop').click(function() {
        $('html, body').animate({scrollTop: 0}, 800);
        return false;
    });
    
    // Smooth Scrolling
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });
    
    // Navbar Scroll Effect
    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('.navbar').addClass('shadow-sm');
        } else {
            $('.navbar').removeClass('shadow-sm');
        }
    });
    
    // Loading Spinner for Forms
    $('form').on('submit', function() {
        var submitBtn = $(this).find('button[type="submit"], input[type="submit"]');
        var originalText = submitBtn.html() || submitBtn.val();
        
        if (submitBtn.length) {
            submitBtn.prop('disabled', true);
            if (submitBtn.is('button')) {
                submitBtn.html('<span class="spinner-border spinner-border-sm me-2"></span>Gönderiliyor...');
            } else {
                submitBtn.val('Gönderiliyor...');
            }
            
            // Reset after 10 seconds (failsafe)
            setTimeout(function() {
                submitBtn.prop('disabled', false);
                if (submitBtn.is('button')) {
                    submitBtn.html(originalText);
                } else {
                    submitBtn.val(originalText);
                }
            }, 10000);
        }
    });
    
    // Image Lazy Loading
    $('img[data-src]').each(function() {
        var img = $(this);
        img.attr('src', img.data('src')).removeAttr('data-src');
    });
    
    // Tooltip Initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Popover Initialization
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide Alerts
    $('.alert').each(function() {
        var alert = $(this);
        setTimeout(function() {
            alert.fadeOut();
        }, 5000);
    });
    
    // Phone Number Formatting
    $('input[type="tel"], input[name*="phone"]').on('input', function() {
        var value = $(this).val().replace(/\D/g, '');
        if (value.length >= 10) {
            var formatted = value.replace(/(\d{3})(\d{3})(\d{2})(\d{2})/, '($1) $2 $3 $4');
            $(this).val(formatted);
        }
    });
    
    // Form Validation Enhancement
    $('form').on('submit', function(e) {
        var form = $(this);
        var isValid = true;
        
        // Required field validation
        form.find('input[required], textarea[required], select[required]').each(function() {
            var field = $(this);
            var value = field.val().trim();
            
            if (!value) {
                isValid = false;
                field.addClass('is-invalid');
                
                // Show error message
                var errorMsg = field.next('.invalid-feedback');
                if (!errorMsg.length) {
                    field.after('<div class="invalid-feedback">Bu alan zorunludur.</div>');
                }
            } else {
                field.removeClass('is-invalid');
                field.next('.invalid-feedback').remove();
            }
        });
        
        // Email validation
        form.find('input[type="email"]').each(function() {
            var field = $(this);
            var value = field.val().trim();
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (value && !emailRegex.test(value)) {
                isValid = false;
                field.addClass('is-invalid');
                
                var errorMsg = field.next('.invalid-feedback');
                if (!errorMsg.length) {
                    field.after('<div class="invalid-feedback">Geçerli bir e-posta adresi giriniz.</div>');
                }
            } else if (value) {
                field.removeClass('is-invalid');
                field.next('.invalid-feedback').remove();
            }
        });
        
        // Phone validation
        form.find('input[type="tel"], input[name*="phone"]').each(function() {
            var field = $(this);
            var value = field.val().replace(/\D/g, '');
            
            if (field.prop('required') && value.length < 10) {
                isValid = false;
                field.addClass('is-invalid');
                
                var errorMsg = field.next('.invalid-feedback');
                if (!errorMsg.length) {
                    field.after('<div class="invalid-feedback">Geçerli bir telefon numarası giriniz.</div>');
                }
            } else if (value.length >= 10) {
                field.removeClass('is-invalid');
                field.next('.invalid-feedback').remove();
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            
            // Focus on first invalid field
            form.find('.is-invalid').first().focus();
            
            // Show error toast
            showToast('Lütfen tüm zorunlu alanları doğru şekilde doldurunuz.', 'error');
        }
    });
    
    // Real-time field validation
    $('input, textarea, select').on('blur', function() {
        var field = $(this);
        var value = field.val().trim();
        
        // Required field check
        if (field.prop('required') && !value) {
            field.addClass('is-invalid');
            if (!field.next('.invalid-feedback').length) {
                field.after('<div class="invalid-feedback">Bu alan zorunludur.</div>');
            }
        } else {
            field.removeClass('is-invalid');
            field.next('.invalid-feedback').remove();
        }
        
        // Email validation
        if (field.attr('type') === 'email' && value) {
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                field.addClass('is-invalid');
                if (!field.next('.invalid-feedback').length) {
                    field.after('<div class="invalid-feedback">Geçerli bir e-posta adresi giriniz.</div>');
                }
            }
        }
    });
    
    // Copy to Clipboard
    $('.copy-to-clipboard').on('click', function() {
        var text = $(this).data('text') || $(this).text();
        
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(function() {
                showToast('Panoya kopyalandı!', 'success');
            });
        } else {
            // Fallback for older browsers
            var textArea = document.createElement("textarea");
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {
                document.execCommand('copy');
                showToast('Panoya kopyalandı!', 'success');
            } catch (err) {
                showToast('Kopyalama başarısız!', 'error');
            }
            document.body.removeChild(textArea);
        }
    });
    
    // Search Functionality
    $('#searchForm').on('submit', function(e) {
        var query = $('#searchInput').val().trim();
        if (!query) {
            e.preventDefault();
            showToast('Lütfen arama yapmak için bir kelime giriniz.', 'warning');
            $('#searchInput').focus();
        }
    });
    
    // Auto-complete Search
    $('#searchInput').on('input', function() {
        var query = $(this).val().trim();
        
        if (query.length >= 2) {
            // Debounce search
            clearTimeout($(this).data('timeout'));
            $(this).data('timeout', setTimeout(function() {
                performSearch(query);
            }, 300));
        }
    });
    
    function performSearch(query) {
        // AJAX search implementation would go here
        console.log('Searching for:', query);
    }
    
    // Image Error Handling
    $('img').on('error', function() {
        var img = $(this);
        if (!img.hasClass('error-handled')) {
            img.addClass('error-handled');
            img.attr('src', '/static/images/placeholder.jpg');
            img.attr('alt', 'Resim yüklenemedi');
        }
    });
    
    // Accordion Enhancement
    $('.accordion-button').on('click', function() {
        var icon = $(this).find('.accordion-icon');
        if (icon.length) {
            icon.toggleClass('fa-plus fa-minus');
        }
    });
    
    // Modal Enhancement
    $('.modal').on('shown.bs.modal', function() {
        $(this).find('input:first').focus();
    });
    
    // Print Button
    $('.print-btn').on('click', function() {
        window.print();
    });
    
    // Share Buttons
    $('.share-btn').on('click', function(e) {
        e.preventDefault();
        var platform = $(this).data('platform');
        var url = encodeURIComponent(window.location.href);
        var title = encodeURIComponent(document.title);
        var shareUrl = '';
        
        switch(platform) {
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                break;
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
                break;
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
                break;
            case 'whatsapp':
                shareUrl = `https://api.whatsapp.com/send?text=${title} ${url}`;
                break;
        }
        
        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
    });
    
    // Rating Stars
    $('.rating-stars .star').on('click', function() {
        var rating = $(this).data('rating');
        var container = $(this).closest('.rating-stars');
        
        container.find('.star').removeClass('active');
        container.find('.star').each(function() {
            if ($(this).data('rating') <= rating) {
                $(this).addClass('active');
            }
        });
        
        container.find('input[type="hidden"]').val(rating);
    });
    
    // Counter Animation
    function animateCounters() {
        $('.counter').each(function() {
            var counter = $(this);
            var target = parseInt(counter.text());
            
            if (target > 0) {
                counter.prop('Counter', 0).animate({
                    Counter: target
                }, {
                    duration: 2000,
                    easing: 'swing',
                    step: function(now) {
                        counter.text(Math.ceil(now));
                    }
                });
            }
        });
    }
    
    // Trigger counter animation when in view
    $(window).on('scroll', function() {
        $('.counter').each(function() {
            var counter = $(this);
            var elementTop = counter.offset().top;
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            
            if (elementTop < viewportBottom && elementTop > viewportTop && !counter.hasClass('animated')) {
                counter.addClass('animated');
                animateCounters();
            }
        });
    });
    
    // File Upload Preview
    $('input[type="file"]').on('change', function() {
        var input = this;
        var preview = $(input).siblings('.file-preview');
        
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            
            reader.onload = function(e) {
                if (preview.length) {
                    preview.html(`<img src="${e.target.result}" class="img-fluid rounded" style="max-height: 200px;">`);
                }
            };
            
            reader.readAsDataURL(input.files[0]);
        }
    });
});

// Utility Functions
function showToast(message, type = 'info') {
    var toastClass = 'bg-primary';
    var icon = 'fas fa-info-circle';
    
    switch(type) {
        case 'success':
            toastClass = 'bg-success';
            icon = 'fas fa-check-circle';
            break;
        case 'error':
            toastClass = 'bg-danger';
            icon = 'fas fa-exclamation-circle';
            break;
        case 'warning':
            toastClass = 'bg-warning text-dark';
            icon = 'fas fa-exclamation-triangle';
            break;
    }
    
    var toastHtml = `
        <div class="toast align-items-center text-white ${toastClass} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="${icon} me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    // Create toast container if it doesn't exist
    if (!$('#toastContainer').length) {
        $('body').append('<div id="toastContainer" class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 9999;"></div>');
    }
    
    var toastElement = $(toastHtml);
    $('#toastContainer').append(toastElement);
    
    var toast = new bootstrap.Toast(toastElement[0]);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.on('hidden.bs.toast', function() {
        $(this).remove();
    });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('tr-TR', {
        style: 'currency',
        currency: 'TRY'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('tr-TR').format(new Date(date));
}

function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Global AJAX Setup
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}