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

    socket.on('booking_cancelled', (data) => {
        alert(`Your ${data.room} booking in ${data.hotelName} has been cancelled.`)
    })

    socket.on('new_user_registered', (username) => {
        alert(`New user registered: ${username}`)
    })
    
   

});