// Main JavaScript for SpeedyCourier

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Track form submission
    const trackForm = document.getElementById('trackForm');
    if (trackForm) {
        trackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const trackingNumber = document.getElementById('trackingNumber').value.trim();
            if (trackingNumber) {
                window.location.href = `/track?tracking_number=${encodeURIComponent(trackingNumber)}`;
            }
        });
    }

    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.classList.add('animate-fade-in-up');
            }
        });
    };

    // Run once on page load
    animateOnScroll();
    
    // Run on scroll
    window.addEventListener('scroll', animateOnScroll);

    // Back to top button
    const backToTopButton = document.getElementById('backToTop');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });

        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('show');
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (mobileMenu && mobileMenuButton) {
            if (!mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
                mobileMenu.classList.remove('show');
            }
        }
    });

    // Initialize map if on contact page
    if (document.getElementById('map')) {
        initMap();
    }
});

// Google Maps initialization
function initMap() {
    // Replace with your actual coordinates
    const location = { lat: -25.9965, lng: 28.1369 }; // Midrand coordinates
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: location,
        styles: [
            {
                "featureType": "all",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "weight": "2.00"
                    }
                ]
            },
            {
                "featureType": "all",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#9c9c9c"
                    }
                ]
            },
            {
                "featureType": "all",
                "elementType": "labels.text",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "landscape",
                "elementType": "all",
                "stylers": [
                    {
                        "color": "#f2f2f2"
                    }
                ]
            },
            {
                "featureType": "landscape",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "landscape.man_made",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "all",
                "stylers": [
                    {
                        "saturation": -100
                    },
                    {
                        "lightness": 45
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#eeeeee"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#7b7b7b"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "transit",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "all",
                "stylers": [
                    {
                        "color": "#46bcec"
                    },
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#c8d7d4"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#070707"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            }
        ]
    });
    
    // Add a marker at the location
    new google.maps.Marker({
        position: location,
        map: map,
        title: 'SpeedyCourier Headquarters',
        icon: {
            url: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png'
        }
    });
}

// Function to format dates
function formatDate(dateString) {
    if (!dateString) return '';
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Format all dates on the page
document.addEventListener('DOMContentLoaded', function() {
    const dateElements = document.querySelectorAll('.format-date');
    dateElements.forEach(element => {
        if (element.textContent) {
            element.textContent = formatDate(element.textContent);
        }
    });
});

// Function to update tracking status
function updateTrackingStatus(trackingNumber) {
    // This would be an API call in a real application
    console.log(`Fetching status for tracking number: ${trackingNumber}`);
    
    // Simulate API call
    setTimeout(() => {
        // This is just a simulation - in a real app, you would update the DOM with real data
        const statusElement = document.getElementById('trackingStatus');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="alert alert-info">
                    <h5>Tracking #${trackingNumber}</h5>
                    <p><strong>Status:</strong> In Transit</p>
                    <p><strong>Last Update:</strong> ${new Date().toLocaleString()}</p>
                    <p><strong>Estimated Delivery:</strong> ${new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toLocaleDateString()}</p>
                </div>
                <div class="tracking-timeline mt-4">
                    <div class="tracking-step completed">
                        <div class="tracking-step-icon"><i class="fas fa-check"></i></div>
                        <div class="tracking-step-content">
                            <h6>Order Received</h6>
                            <p>${new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toLocaleString()}</p>
                        </div>
                    </div>
                    <div class="tracking-step completed">
                        <div class="tracking-step-icon"><i class="fas fa-check"></i></div>
                        <div class="tracking-step-content">
                            <h6>In Transit</h6>
                            <p>${new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toLocaleString()}</p>
                        </div>
                    </div>
                    <div class="tracking-step active">
                        <div class="tracking-step-icon"><i class="fas fa-truck"></i></div>
                        <div class="tracking-step-content">
                            <h6>Out for Delivery</h6>
                            <p>${new Date().toLocaleString()}</p>
                        </div>
                    </div>
                    <div class="tracking-step">
                        <div class="tracking-step-icon"><i class="far fa-clock"></i></div>
                        <div class="tracking-step-content">
                            <h6>Delivered</h6>
                            <p>Estimated: ${new Date(Date.now() + 1 * 24 * 60 * 60 * 1000).toLocaleDateString()}</p>
                        </div>
                    </div>
                </div>
            `;
        }
    }, 1000);
}

// Initialize tracking if on tracking page
const urlParams = new URLSearchParams(window.location.search);
const trackingNumber = urlParams.get('tracking_number');
if (trackingNumber) {
    updateTrackingStatus(trackingNumber);
}

// Function to handle contact form submission
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(contactForm);
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });
        
        // In a real app, you would send this to your server
        console.log('Form submitted:', formObject);
        
        // Show success message
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success mt-3';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = 'Thank you for your message! We will get back to you soon.';
        
        contactForm.reset();
        contactForm.appendChild(alertDiv);
        
        // Scroll to the alert
        alertDiv.scrollIntoView({ behavior: 'smooth' });
        
        // Remove the alert after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    });
}
