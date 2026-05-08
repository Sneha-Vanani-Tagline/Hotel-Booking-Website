window.addEventListener('load', function() {

    const all_btn = this.document.querySelector('#allFilter');
    const upcoming_btn = this.document.querySelector('#upcomingFilter');
    const complete_btn = this.document.querySelector('#completedFilter');
    const cancel_btn = this.document.querySelector('#cancelledFilter');
    const booking_card_div = this.document.querySelectorAll('.booking-card-conatiner');
    const buttons = this.document.querySelectorAll(".filter-btn");
    const today_date = getTodayDate();      // return date object, with hours set to 0
    

    function getTodayDate() {
        const date = new Date()
        date.setHours(0, 0, 0, 0)       // set time to 0
        return date
    }

    // buttons change active class
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            buttons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
        });
    });

    // initaillay it render all the bookings
    allBookings()

    // event listener
    all_btn.addEventListener('click', allBookings)
    upcoming_btn.addEventListener('click', upcomingBookings)
    complete_btn.addEventListener('click', completedBookings)
    cancel_btn.addEventListener('click', cancelledBookings)

    function allBookings() {

        booking_card_div.forEach(card => {
            card.classList.remove('hidden');
        })
    }

    function upcomingBookings() {

        booking_card_div.forEach(card => {
        
            let checkoutF = card.querySelector('.checkout').dataset.checkout       // written 'card' instead of 'document' becuase i want to search inside that specific element, not it whole document
            let checkout_date = new Date(checkoutF)
            checkout_date.setHours(0,0,0,0)

            if (card.dataset.status === 'confirmed' && checkout_date >= today_date) {
                card.classList.remove('hidden');
            }
            else {
                card.classList.add('hidden');
            }
        })
    }

    function completedBookings() {
        booking_card_div.forEach(card => {

            let checkoutF = card.querySelector('.checkout').dataset.checkout;      
            let checkout_date = new Date(checkoutF)
            checkout_date.setHours(0,0,0,0)

            if (checkout_date < today_date && card.dataset.status !== 'cancelled') {
                card.classList.remove('hidden')
            }
            else {
                card.classList.add('hidden')
            }
        })
    }

    function cancelledBookings() {

        booking_card_div.forEach(card => {
            if (card.dataset.status === 'cancelled') {
                card.classList.remove('hidden');
            }
            else {
                card.classList.add('hidden');
            }
        })
    }
})

