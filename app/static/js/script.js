window.addEventListener('load', () => {

    const checkin_search = document.querySelector('#search-checkin');
    const checkout_search = document.querySelector('#search-checkout');

    const today = new Date().toISOString().split("T")[0];

    console.log("JS");
    
    // search setting date
    checkin_search.min = today;

    checkin_search.addEventListener('change', () => {
        checkout_search.min = checkin_search.value
    })

    checkout_search.addEventListener('change', () => {
        checkin_date = new Date(checkin_search.value)
        checkout_date = new Date(checkout_search.value)

        if (checkin_date > checkout_date) {
            alert('Checkout date must be greater that Checkin!')
        }
    })
    // checkout.min = checkin.value;
})