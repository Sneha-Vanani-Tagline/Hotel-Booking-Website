
window.addEventListener('load', () => {

    console.log('Socket JS')

    // web socket 
    window.socket = io();

    socket.on('connect', () => {
        console.log('Socket connected.')

        console.log('USER ID:', window.userId);
        console.log('ROLE:', window.userRole);
        if (window.userId) {
            if(window.userRole == 'user') {
                console.log('EMIT JOIN USER');
                socket.emit('join_user', window.userId);
            }
            else if(window.userRole == 'host') {
                console.log('EMIT JOIN host');
                socket.emit('join_host', window.userId);
            }
            else if(window.userRole == 'admin') {
                console.log('EMIT JOIN admin');
                socket.emit('join_admin');
            }
        }
    })

    
    socket.on('message', (data) => {
        console.log('Message: ',data)
    })

    socket.on('new_booking', (data) => {
        console.log(data.bookerName, data.hotelName)
        alert(`${data['bookerName']} has booked room in your ${data['hotelName']}.`)
    })

    socket.on('booking_created', (data) => {
        
        alert(`You have new booking in ${data.hotelName}, booked by: ${data.bookerName}`)
        
        if (window.location.pathname == '/admin/bookinglist' || 
            window.location.pathname == '/booking/allBookings' ) 
        {
            location.reload()
        }
    })

    socket.on('booking_cancelled', (data) => {
        alert(`Your ${data.room} booking in ${data.hotelName} has been cancelled.`)
    
        if (window.location.pathname == '/admin/bookinglist' ||
            window.location.pathname == '/booking/allBookings'
        ) {
            location.reload()
        }
    })

    socket.on('update_myBookings', () => {
        if(window.location.pathname == '/booking/myBookings') {
            location.reload();
        }
    })

    socket.on('update_host_dashboard', () => {
        if (window.location.pathname == '/host/dashboard') {
            location.reload();
        }
        
    })

    socket.on('update_admin_dashboard', () => {
        if (window.location.pathname == '/admin/dashboard') {
            location.reload();
        }
    })

    socket.on('update_hotellist', () => {
        if (window.location.pathname == '/admin/hotellist') {
            location.reload();
        }
    })

    

    socket.on('new_user_registered', (username) => {
        alert(`New user registered: ${username}`)

        if (window.location.pathname == '/admin/userlist') {
            location.reload()
        }
    })
    
    // Socket event
    window.socket.on('render_message_page', (cid) => {

        window.location.href = `/chat/${window.userId}?conversation=${cid}`
    })

    socket.on('update_actionLogs', () => {
        if (window.location.pathname == '/admin/audit-logs') {
            location.reload();
            console.log('Audit : Audit Log Update');

        }
    })

    // notifiy user for new message
    const chat_notification_dot = document.querySelector('.notification-dot');

    socket.on('display_msg_notification', (has_unread_msg) => {
        
        if (has_unread_msg == 0){
            chat_notification_dot.classList.add('hidden');
        }
        else {

            chat_notification_dot.classList.remove('hidden');
            chat_notification_dot.innerText = has_unread_msg
        }
    })

    // socket.onAny((event, ...args) => {
    //     console.log('RECEIVED EVENT:', event, args);
    // });
    

});