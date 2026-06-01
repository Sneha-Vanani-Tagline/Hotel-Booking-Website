window.addEventListener('load', () => {

    console.log('Chat JS')
    const conversation_a = document.querySelectorAll('.conversation-link')
    const active_chat_div = document.querySelector('.active-chat-div')
    const active_chat_placeholder = document.querySelector('.active-chat-placeholder')
    const chat_condition = document.querySelector('#chat_condition');
    const send_btn = document.querySelector('#msd-send-btn');
    const msg_input_box = document.querySelector('#input-box');
    const sender_role = document.querySelector('#sender');
    const chat_body = document.querySelector('.chat-body');
    const chat_header = document.querySelector('#active-chat-header');
    const chat_notification_dot = document.querySelector('.notification-dot');
    const msg_input_container = document.querySelector('.chat-input-area')
    
   let active_cid = null;

    // Conversation click event
    conversation_a.forEach(c => {
        c.addEventListener('click', (e) => {
            e.preventDefault();
            
            console.log('in conversation button click event');
            let fullId = c.id;
            let cid = fullId.split('_')[1];
            let selected_Conversion = document.querySelector(`#${fullId}`);

            chat_process(cid, selected_Conversion)

        })
    });


    // Manually clicks on conversation on "Message Host" button click
    const params = new URLSearchParams(window.location.search);
    let cid = params.get('conversation');
    console.log('Conversation id: ',cid);
    
    if (cid){
        console.log('cid found')
        let conversation = document.querySelector(`#conver_${cid}`)
        
        if (conversation) {
            conversation.click();
        }
    }

    // Socket Event to render new Messages
    socket.on('render_new_chat_message', (data) => {
        console.log('render_new_chat_message event in JS', data, active_cid)

        let msgSent_by = ''  //sender or reciever

        if (data['sender'] == userRole) {
            msgSent_by = 'sender'
        }
        else {
            msgSent_by = 'receiver'
        }

        if(window.location.pathname == `/chat/${userId}` && data['conversation_id'] == active_cid) {
            
            let html = `
                <div class="message-wrapper ${msgSent_by}" data-converid="${data['conversation_id']}">

                    <div class="message">

                        <p>${data['msg']}</p>

                        <small>
                            ${data['created_at']}
                        </small>

                    </div>
                </div>
            `
            chat_body.innerHTML += html;

            chat_notification_dot.classList.add('hidden');


            // Scroll to newest message
            chat_body.scrollTop = chat_body.scrollHeight;
        }
        
            
    })

    // msg send btn click
    send_btn.addEventListener('click', () => {

        if (!active_cid) return;
        if (!msg_input_box.value) return;

        // console.log('send button Clicked')
        data = {
            'msg': msg_input_box.value,
            'conversation_id': active_cid,
            'sender': sender_role.value
        }

        msg_input_box.value = '';

        socket.emit('new_chat_message', data)

    })

    // Render all the messages of selected Chat
    function chat_process(cid, selected_Conversion) {

        const allChats = document.querySelectorAll('.message-wrapper');
        chat_notification_dot.classList.add('hidden');

        active_cid = cid;

        // console.log('in chat_process')
        active_chat_placeholder.classList.add('hidden');
        active_chat_div.classList.remove('hidden');
        msg_input_container.classList.remove('hidden');

        allChats.forEach(chat => {
            chat.classList.add('hidden');
        });

        const selectedChat = document.querySelectorAll(`[data-converid="${active_cid}"]`)

        if (selected_Conversion.dataset.user) {
            chat_header.innerText = selected_Conversion.dataset.user;
        }
        else if (selected_Conversion.dataset.hotel) {
            chat_header.innerText = selected_Conversion.dataset.hotel;
        }
        
        if (selectedChat) {
            selectedChat.forEach(msg => {
                msg.classList.remove('hidden');
            })
        }

        // Scroll to newest message
        chat_body.scrollTop = chat_body.scrollHeight;

        socket.emit('makeAll_msg_asRead', active_cid, userRole)
        
    }

});


