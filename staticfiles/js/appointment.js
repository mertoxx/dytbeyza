// static/js/appointment.js

$(document).ready(function() {
    
    // Tarih seçimi değiştiğinde müsait saatleri getir
    $('#id_appointment_date').on('change', function() {
        var selectedDate = $(this).val();
        var timeSelect = $('#id_appointment_time');
        
        if (selectedDate) {
            // Loading state
            timeSelect.html('<option value="">Yükleniyor...</option>');
            timeSelect.prop('disabled', true);
            
            // AJAX request to get available times
            $.ajax({
                url: '/randevular/ajax/musait-saatler/',
                type: 'GET',
                data: {
                    'date': selectedDate
                },
                success: function(data) {
                    timeSelect.html('<option value="">Saat seçin</option>');
                    
                    if (data.times && data.times.length > 0) {
                        $.each(data.times, function(index, time) {
                            timeSelect.append(`<option value="${time.id}">${time.time}</option>`);
                        });
                        timeSelect.prop('disabled', false);
                    } else {
                        timeSelect.html('<option value="">Bu tarihte müsait saat yok</option>');
                        showToast('Seçtiğiniz tarihte müsait saat bulunmamaktadır. Lütfen başka bir tarih seçin.', 'warning');
                    }
                },
                error: function() {
                    timeSelect.html('<option value="">Hata oluştu</option>');
                    showToast('Saatler yüklenirken bir hata oluştu. Lütfen tekrar deneyin.', 'error');
                }
            });
        } else {
            timeSelect.html('<option value="">Önce tarih seçin</option>');
            timeSelect.prop('disabled', true);
        }
    });
    
    // BMI Hesaplama
    function calculateBMI() {
        var height = parseFloat($('#id_height').val());
        var weight = parseFloat($('#id_weight').val());
        
        if (height && weight && height > 0) {
            var heightM = height / 100;
            var bmi = weight / (heightM * heightM);
            var bmiText = '';
            var bmiClass = '';
            
            if (bmi < 18.5) {
                bmiText = 'Düşük kilolu';
                bmiClass = 'text-info';
            } else if (bmi < 25) {
                bmiText = 'Normal kilolu';
                bmiClass = 'text-success';
            } else if (bmi < 30) {
                bmiText = 'Fazla kilolu';
                bmiClass = 'text-warning';
            } else {
                bmiText = 'Obez';
                bmiClass = 'text-danger';
            }
            
            // BMI gösterimi
            if (!$('#bmi-display').length) {
                $('#id_weight').after(`
                    <div id="bmi-display" class="mt-2">
                        <small class="text-muted">BMI: <span id="bmi-value" class="${bmiClass}"></span></small>
                    </div>
                `);
            }
            
            $('#bmi-value').text(`${bmi.toFixed(1)} (${bmiText})`).attr('class', bmiClass);
        } else {
            $('#bmi-display').remove();
        }
    }
    
    // Boy ve kilo değişikliklerinde BMI hesapla
    $('#id_height, #id_weight').on('input', calculateBMI);
    
    // Tarih validasyonu - geçmiş tarih seçilememeli
    var today = new Date().toISOString().split('T')[0];
    $('#id_appointment_date').attr('min', today);
    
    // Telefon numarası formatlaması
    $('#id_phone').on('input', function() {
        var value = $(this).val().replace(/\D/g, '');
        var formatted = '';
        
        if (value.startsWith('90')) {
            value = value.substring(2);
        }
        
        if (value.length >= 10) {
            formatted = '+90 ' + value.substring(0, 3) + ' ' + 
                       value.substring(3, 6) + ' ' + 
                       value.substring(6, 8) + ' ' + 
                       value.substring(8, 10);
        } else if (value.length > 0) {
            formatted = '+90 ' + value;
        }
        
        $(this).val(formatted);
    });
    
    // Yaş validasyonu
    $('#id_age').on('input', function() {
        var age = parseInt($(this).val());
        if (age < 15 || age > 100) {
            $(this).addClass('is-invalid');
            if (!$(this).next('.invalid-feedback').length) {
                $(this).after('<div class="invalid-feedback">Yaş 15-100 arasında olmalıdır.</div>');
            }
        } else {
            $(this).removeClass('is-invalid');
            $(this).next('.invalid-feedback').remove();
        }
    });
    
    // Boy validasyonu
    $('#id_height').on('input', function() {
        var height = parseInt($(this).val());
        if (height < 100 || height > 250) {
            $(this).addClass('is-invalid');
            if (!$(this).next('.invalid-feedback').length) {
                $(this).after('<div class="invalid-feedback">Boy 100-250 cm arasında olmalıdır.</div>');
            }
        } else {
            $(this).removeClass('is-invalid');
            $(this).next('.invalid-feedback').remove();
        }
    });
    
    // Kilo validasyonu
    $('#id_weight').on('input', function() {
        var weight = parseFloat($(this).val());
        if (weight < 30 || weight > 300) {
            $(this).addClass('is-invalid');
            if (!$(this).next('.invalid-feedback').length) {
                $(this).after('<div class="invalid-feedback">Kilo 30-300 kg arasında olmalıdır.</div>');
            }
        } else {
            $(this).removeClass('is-invalid');
            $(this).next('.invalid-feedback').remove();
        }
    });
    
    // Form gönderimi öncesi validasyon
    $('#appointment-form').on('submit', function(e) {
        var isValid = true;
        var firstInvalidField = null;
        
        // Tarih kontrolü
        var selectedDate = $('#id_appointment_date').val();
        if (!selectedDate) {
            isValid = false;
            $('#id_appointment_date').addClass('is-invalid');
            if (!firstInvalidField) firstInvalidField = $('#id_appointment_date');
        }
        
        // Saat kontrolü
        var selectedTime = $('#id_appointment_time').val();
        if (!selectedTime) {
            isValid = false;
            $('#id_appointment_time').addClass('is-invalid');
            if (!firstInvalidField) firstInvalidField = $('#id_appointment_time');
        }
        
        // Telefon kontrolü
        var phone = $('#id_phone').val().replace(/\D/g, '');
        if (phone.length < 10) {
            isValid = false;
            $('#id_phone').addClass('is-invalid');
            if (!firstInvalidField) firstInvalidField = $('#id_phone');
        }
        
        // Hedefler kontrolü
        var goals = $('#id_goals').val().trim();
        if (goals.length < 10) {
            isValid = false;
            $('#id_goals').addClass('is-invalid');
            if (!$('#id_goals').next('.invalid-feedback').length) {
                $('#id_goals').after('<div class="invalid-feedback">Lütfen hedeflerinizi daha detaylı açıklayın (en az 10 karakter).</div>');
            }
            if (!firstInvalidField) firstInvalidField = $('#id_goals');
        }
        
        if (!isValid) {
            e.preventDefault();
            
            if (firstInvalidField) {
                firstInvalidField.focus();
                
                // Smooth scroll to first invalid field
                $('html, body').animate({
                    scrollTop: firstInvalidField.offset().top - 100
                }, 500);
            }
            
            showToast('Lütfen tüm zorunlu alanları doğru şekilde doldurunuz.', 'error');
        } else {
            // Show loading message
            showToast('Randevu talebiniz gönderiliyor...', 'info');
        }
    });
    
    // Character counter for textarea fields
    $('textarea').each(function() {
        var textarea = $(this);
        var maxLength = textarea.attr('maxlength');
        
        if (maxLength) {
            var counterId = textarea.attr('id') + '-counter';
            textarea.after(`<small id="${counterId}" class="text-muted float-end"></small>`);
            
            function updateCounter() {
                var remaining = maxLength - textarea.val().length;
                $(`#${counterId}`).text(`${remaining} karakter kaldı`);
                
                if (remaining < 20) {
                    $(`#${counterId}`).removeClass('text-muted').addClass('text-warning');
                } else {
                    $(`#${counterId}`).removeClass('text-warning').addClass('text-muted');
                }
            }
            
            textarea.on('input', updateCounter);
            updateCounter();
        }
    });
    
    // Gelişmiş form adım navigasyonu (isteğe bağlı)
    if ($('.form-step').length > 1) {
        var currentStep = 0;
        var totalSteps = $('.form-step').length;
        
        function showStep(step) {
            $('.form-step').hide();
            $(`.form-step:eq(${step})`).show();
            
            // Progress bar güncelle
            var progress = ((step + 1) / totalSteps) * 100;
            $('.progress-bar').css('width', progress + '%');
            
            // Button states
            $('#prevBtn').toggle(step > 0);
            $('#nextBtn').toggle(step < totalSteps - 1);
            $('#submitBtn').toggle(step === totalSteps - 1);
        }
        
        $('#nextBtn').on('click', function() {
            if (validateCurrentStep()) {
                currentStep++;
                showStep(currentStep);
            }
        });
        
        $('#prevBtn').on('click', function() {
            currentStep--;
            showStep(currentStep);
        });
        
        function validateCurrentStep() {
            var currentStepElement = $(`.form-step:eq(${currentStep})`);
            var isValid = true;
            
            currentStepElement.find('input[required], select[required], textarea[required]').each(function() {
                if (!$(this).val().trim()) {
                    isValid = false;
                    $(this).addClass('is-invalid');
                } else {
                    $(this).removeClass('is-invalid');
                }
            });
            
            return isValid;
        }
        
        // Initialize
        showStep(0);
    }
    
    // Auto-save draft (local storage)
    function saveDraft() {
        var formData = {};
        $('#appointment-form input, #appointment-form select, #appointment-form textarea').each(function() {
            var field = $(this);
            if (field.attr('type') !== 'hidden' && field.attr('name')) {
                formData[field.attr('name')] = field.val();
            }
        });
        
        localStorage.setItem('appointment_draft', JSON.stringify(formData));
        showToast('Taslak kaydedildi', 'success');
    }
    
    function loadDraft() {
        var draft = localStorage.getItem('appointment_draft');
        if (draft) {
            try {
                var formData = JSON.parse(draft);
                Object.keys(formData).forEach(function(key) {
                    var field = $(`[name="${key}"]`);
                    if (field.length && formData[key]) {
                        field.val(formData[key]);
                    }
                });
                
                showToast('Taslak yüklendi', 'info');
            } catch (e) {
                console.error('Draft loading error:', e);
            }
        }
    }
    
    // Load draft on page load
    if (localStorage.getItem('appointment_draft')) {
        $('<button type="button" class="btn btn-outline-secondary mb-3" id="loadDraftBtn">Kayıtlı Taslağı Yükle</button>')
            .insertBefore('#appointment-form');
        
        $('#loadDraftBtn').on('click', function() {
            loadDraft();
            $(this).remove();
        });
    }
    
    // Auto-save every 30 seconds
    setInterval(function() {
        var hasData = false;
        $('#appointment-form input, #appointment-form textarea').each(function() {
            if ($(this).val().trim()) {
                hasData = true;
                return false;
            }
        });
        
        if (hasData) {
            saveDraft();
        }
    }, 30000);
    
    // Clear draft on successful submission
    $('#appointment-form').on('submit', function() {
        setTimeout(function() {
            localStorage.removeItem('appointment_draft');
        }, 1000);
    });
});

// Utility function for appointment form
function showAppointmentToast(message, type = 'info') {
    showToast(message, type);
}