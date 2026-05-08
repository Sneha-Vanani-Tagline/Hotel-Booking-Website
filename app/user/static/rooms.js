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
        // fetching search input
        let price = Number(filter_price_slider.value);
        let guest = Number(filter_guest.value);
        let rooms = Number(filter_rooms.value);
        let facility = [];

        for (let check of filter_facility_check) {
            if (check.checked) {
                facility.push(check.value);
            }
        }

        console.log(price, guest, rooms, facility);

            room_div.forEach(room => {
                // fetching room data
                let room_price = Number(room.querySelector('.price').dataset.price);
                let room_guest = Number(room.querySelector('.guest').dataset.guest);
                let room_rooms = Number(room.querySelector('.rooms').dataset.rooms);
                let room_facilities = room.querySelectorAll('.facility');
                
                let room_facility_arr = [];
                let isvisible = true
                // creating room facilities array
                room_facilities.forEach(f => {
                    room_facility_arr.push(f.dataset.facility);
                })

                room.classList.add('hidden');
                
                // price filter
                if (room_price > price) {
                    isvisible = false;
                }

                // guest filter
                if (room_guest != 0 && room_guest < guest) {
                    isvisible = false;
                }

                // rooms filter
                if (rooms != 0 && room_rooms != rooms) {
                    isvisible = false;
                }

                // facility filter
                if (facility) {
                    facility.forEach(f => {
                        if (!room_facility_arr.includes(f)) {
                            isvisible = false
                        }
                    })
                }

                if (isvisible) {
                    console.log('true part')
                    room.classList.remove('hidden');
                }
            });

    })
})