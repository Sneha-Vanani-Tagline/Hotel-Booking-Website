window.addEventListener('load', function() {
    
    const bookingF = this.document.querySelector('#booking_form')
    const checkinF = this.document.querySelector('#checkin_field')
    const checkoutF = this.document.querySelector('#checkout_field')
    const nightsF = this.document.querySelector('#nights')
    const totalPriceF = this.document.querySelector('#totalPrice')
    const pricePerNight = this.document.querySelector('#price');

    const today = new Date().toISOString().split("T")[0];
    console.log("today date ",today)
    checkinF.min = today

    function validateDates() {
        console.log('date change event')
        if (!checkinF.value || !checkoutF.value) {
            totalPriceF.value = 0;
            nightsF.innerText = 0;
            return
        }

        const checkin_date = new Date(checkinF.value)
        const checkout_date = new Date(checkoutF.value)

        // Validation: checkout must be after checkin
        if (checkout_date <= checkin_date) {
            alert("Checkout date must be after check-in date");
            checkoutF.value = ''
            totalPriceF.value = 0;
            nightsF.innerText = 0;
            return
        }
        
        // calculate nights
        const duration = checkout_date - checkin_date;  // gives result in miliseconds
        const oneDay = 1000 * 60 * 60 * 24;
        const nights = duration / oneDay;
        nightsF.innerText = nights;

        // calculate total price
        const total = nights * pricePerNight.dataset.price;
        totalPriceF.value = total;

        console.log(nights, total)
    }

    checkinF.addEventListener('change', function() {
        checkoutF.min = checkinF.value
        validateDates()
    })
    checkoutF.addEventListener('change', validateDates)

})