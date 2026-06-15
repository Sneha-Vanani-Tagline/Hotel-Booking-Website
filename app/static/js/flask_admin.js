window.addEventListener('load', () => {

    console.log('JS connected...')

    $('#hotel').change(function() {
        let hotel = $(this).val();

        $.getJSON('/admin/hotel-rooms/' + hotel, function(data) {

            let rooms = $('#rooms');
            rooms.empty();

            $.each(data, function(i, item) {
                rooms.append(
                    $('<option>', {
                        value: item.id,
                        text: item.category
                    })
                )
            })
        })
    })
})