window.addEventListener('load', () => {

    // -------------- filter ------------
    const filterBtn = document.querySelector('#filterToggle');
    const filterContainer = document.querySelector('#filterPanel');
    const filter_price_slider = document.querySelector('#filter-price-slider');
    const filter_guest = document.querySelector('#filter-guest');
    const filter_rooms = document.querySelector('#filter-rooms');
    const filter_facility_check = document.querySelectorAll('.filter-facility');
    const priceValue = document.querySelector('#priceValue');
    const apply_filter = document.querySelector('#apply-filter');
    const room_div = document.querySelectorAll('.room_container');
    
    
    console.log('JS')
    // filter toggle
    filterBtn.addEventListener('click', () => {
        
        filterContainer.classList.toggle('active');
    });

    filter_price_slider.addEventListener('input', () => {
        priceValue.innerText = filter_price_slider.value;
    })

    apply_filter.addEventListener('click', () => {
        let price = Number(filter_price_slider.value)
        let guest = Number(filter_guest.value)
        let rooms = Number(filter_rooms.value);
        let facility = [];

        for (let check of filter_facility_check) {
            if (check.checked) {
                facility.push(check.value);
            }
        }

        console.log(price, guest, rooms, facility);

            // work is pending
            room_div.forEach(room => {
                let room_price = room.querySelector('.price').dataset.price;
                let room_guest = room.querySelector('.guest').dataset.guest;
                let room_rooms = room.querySelector('.rooms').dataset.rooms;
                let isvisible = true

                room.classList.add('hidden');
                console.log(room_price, room_guest, room_rooms);

                if (price == 20000 && Number(room_price) > price) {
                    isvisible = false
                }

                if (room_guest < guest) {
                    isvisible = false
                }

                if (room_rooms < room) {
                    isvisible = false
                }

                if (isvisible) {
                    room.classList.remove('hidden');
                }
            });

    })
})